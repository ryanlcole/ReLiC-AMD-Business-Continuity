#pragma once
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>

namespace runecore {

constexpr double kG = 1.0;
constexpr double kSoftening2 = 1e-6;
constexpr double kTwoPi = 6.283185307179586476925286766559;

struct RuneState {
    double x, y, z;
    double vx, vy, vz;
    double mass;
    double amplitude;
    double phase;
};

struct Derivative {
    double ax, ay, az;
    double potential;
};

struct ShaepCandidate {
    uint32_t a;
    uint32_t b;
    double separation;
    double specific_energy;
    double score;
};

struct Metrics {
    uint64_t count = 0;
    uint64_t steps = 0;
    double dt = 0.0;
    double elapsed_ms = 0.0;
    double kinetic = 0.0;
    double potential = 0.0;
    double total_energy = 0.0;
    double energy_drift = 0.0;
    uint64_t shaep_candidates = 0;
    std::string backend;
    std::string state_sha256;
};

inline uint64_t splitmix64(uint64_t& state) {
    uint64_t z = (state += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}

inline double unit01(uint64_t& s) {
    return (splitmix64(s) >> 11) * (1.0 / 9007199254740992.0);
}

inline std::vector<RuneState> seed_runes(size_t n, uint64_t seed) {
    std::vector<RuneState> r(n);
    uint64_t s = seed;
    for (size_t i = 0; i < n; ++i) {
        const double radius = 0.5 + 4.5 * unit01(s);
        const double angle = kTwoPi * unit01(s);
        const double z = (unit01(s) - 0.5) * 0.2;
        const double mass = 0.5 + unit01(s);
        r[i] = {
            radius * std::cos(angle), radius * std::sin(angle), z,
            -0.12 * std::sin(angle), 0.12 * std::cos(angle), 0.0,
            mass,
            0.05 + 0.05 * unit01(s),
            kTwoPi * unit01(s)
        };
    }
    return r;
}

inline void cpu_derivatives(const std::vector<RuneState>& r, std::vector<Derivative>& d) {
    const size_t n = r.size();
    d.assign(n, {});
    for (size_t i = 0; i < n; ++i) {
        double ax = 0, ay = 0, az = 0, pot = 0;
        for (size_t j = 0; j < n; ++j) {
            if (i == j) continue;
            const double dx = r[j].x - r[i].x;
            const double dy = r[j].y - r[i].y;
            const double dz = r[j].z - r[i].z;
            const double r2 = dx*dx + dy*dy + dz*dz + kSoftening2;
            const double inv_r = 1.0 / std::sqrt(r2);
            const double inv_r3 = inv_r * inv_r * inv_r;
            const double f = kG * r[j].mass * inv_r3;
            ax += dx * f;
            ay += dy * f;
            az += dz * f;
            pot -= kG * r[j].mass * inv_r;
        }
        d[i] = {ax, ay, az, pot};
    }
}

inline void integrate(std::vector<RuneState>& r, const std::vector<Derivative>& d, double dt) {
    for (size_t i = 0; i < r.size(); ++i) {
        auto& q = r[i];
        const auto& a = d[i];
        q.vx += a.ax * dt;
        q.vy += a.ay * dt;
        q.vz += a.az * dt;
        q.x += q.vx * dt;
        q.y += q.vy * dt;
        q.z += q.vz * dt;
        const double speed = std::sqrt(q.vx*q.vx + q.vy*q.vy + q.vz*q.vz);
        const double omega = 1.0 + 0.05 * speed + 0.01 * std::fabs(a.potential);
        q.phase = std::fmod(q.phase + omega * dt, kTwoPi);
        if (q.phase < 0) q.phase += kTwoPi;
        q.amplitude = std::max(0.0, q.amplitude * std::exp(-0.0005 * dt));
    }
}

inline double kinetic_energy(const std::vector<RuneState>& r) {
    double e = 0;
    for (const auto& q : r)
        e += 0.5*q.mass*(q.vx*q.vx+q.vy*q.vy+q.vz*q.vz);
    return e;
}

inline double potential_energy(const std::vector<RuneState>& r) {
    double e = 0;
    for (size_t i=0;i<r.size();++i)
        for(size_t j=i+1;j<r.size();++j) {
            double dx=r[j].x-r[i].x;
            double dy=r[j].y-r[i].y;
            double dz=r[j].z-r[i].z;
            double dist=std::sqrt(dx*dx+dy*dy+dz*dz+kSoftening2);
            e -= kG*r[i].mass*r[j].mass/dist;
        }
    return e;
}

inline std::vector<ShaepCandidate> detect_pair_shaeps(const std::vector<RuneState>& r, double max_sep=0.35) {
    std::vector<ShaepCandidate> out;
    for (size_t i=0;i<r.size();++i)
        for(size_t j=i+1;j<r.size();++j) {
            const double dx=r[j].x-r[i].x;
            const double dy=r[j].y-r[i].y;
            const double dz=r[j].z-r[i].z;
            const double dvx=r[j].vx-r[i].vx;
            const double dvy=r[j].vy-r[i].vy;
            const double dvz=r[j].vz-r[i].vz;
            const double sep=std::sqrt(dx*dx+dy*dy+dz*dz+kSoftening2);
            if (sep > max_sep) continue;
            const double relv2=dvx*dvx+dvy*dvy+dvz*dvz;
            const double mu = (r[i].mass*r[j].mass)/(r[i].mass+r[j].mass);
            const double specific = 0.5*mu*relv2 - kG*r[i].mass*r[j].mass/sep;
            if (specific < 0.0) {
                const double phase_delta = std::fabs(std::remainder(r[i].phase-r[j].phase, kTwoPi));
                const double score = (-specific)/(1.0+phase_delta);
                out.push_back({(uint32_t)i,(uint32_t)j,sep,specific,score});
            }
        }
    std::sort(out.begin(), out.end(), [](auto&a,auto&b){return a.score>b.score;});
    return out;
}

inline void write_state_csv(const std::string& path, const std::vector<RuneState>& r) {
    std::ofstream f(path);
    f << std::setprecision(17);
    f << "id,x,y,z,vx,vy,vz,mass,amplitude,phase\n";
    for(size_t i=0;i<r.size();++i){
        const auto&q=r[i];
        f<<i<<','<<q.x<<','<<q.y<<','<<q.z<<','<<q.vx<<','<<q.vy<<','<<q.vz<<','<<q.mass<<','<<q.amplitude<<','<<q.phase<<'\n';
    }
}

inline std::string json_escape(const std::string& s) {
    std::ostringstream o;
    for(char c:s){
        if(c=='"'||c=='\\') o<<'\\'<<c;
        else if(c=='\n') o<<"\\n";
        else o<<c;
    }
    return o.str();
}

inline void write_metrics_json(const std::string& path, const Metrics& m, const std::vector<ShaepCandidate>& s) {
    std::ofstream f(path);
    f<<std::setprecision(17);
    f << "{\n"
      << "  \"status\": \"OBSERVATION_NOT_CANON\",\n"
      << "  \"backend\": \""<<json_escape(m.backend)<<"\",\n"
      << "  \"count\": "<<m.count<<",\n"
      << "  \"steps\": "<<m.steps<<",\n"
      << "  \"dt\": "<<m.dt<<",\n"
      << "  \"elapsed_ms\": "<<m.elapsed_ms<<",\n"
      << "  \"kinetic\": "<<m.kinetic<<",\n"
      << "  \"potential\": "<<m.potential<<",\n"
      << "  \"total_energy\": "<<m.total_energy<<",\n"
      << "  \"energy_drift\": "<<m.energy_drift<<",\n"
      << "  \"shaep_candidates\": "<<s.size()<<",\n"
      << "  \"warnings\": [\"EXPERIMENTAL_NORMALIZED_MODEL\", \"SHAEP_CANDIDATE_IS_NOT_PHYSICAL_IDENTITY\", \"METADATA_DOES_NOT_CAUSE_STATE\"],\n"
      << "  \"top_candidates\": [";
    for(size_t i=0;i<std::min<size_t>(s.size(),8);++i){
        if(i) f<<',';
        const auto&c=s[i];
        f << "{\"a\":"<<c.a<<",\"b\":"<<c.b<<",\"separation\":"<<c.separation<<",\"specific_energy\":"<<c.specific_energy<<",\"score\":"<<c.score<<"}";
    }
    f << "]\n}\n";
}

} // namespace runecore
