#include "runecore.hpp"
#include <chrono>
#include <cstdlib>
#include <iostream>

int main(int argc, char** argv) {
    size_t n = argc>1 ? std::strtoull(argv[1],nullptr,10) : 1000;
    uint64_t steps = argc>2 ? std::strtoull(argv[2],nullptr,10) : 100;
    double dt = argc>3 ? std::strtod(argv[3],nullptr) : 0.001;
    uint64_t seed = argc>4 ? std::strtoull(argv[4],nullptr,10) : 1;
    std::string prefix = argc>5 ? argv[5] : "evidence/cpu";
    if(n<2 || n>200000 || steps<1 || steps>1000000 || !(dt>0 && dt<=0.1)) {
        std::cerr<<"invalid arguments\n";
        return 2;
    }

    auto state = runecore::seed_runes(n, seed);
    std::vector<runecore::Derivative> d;
    const double e0 = runecore::kinetic_energy(state)+runecore::potential_energy(state);
    auto t0=std::chrono::steady_clock::now();
    for(uint64_t step=0;step<steps;++step){
        runecore::cpu_derivatives(state,d);
        runecore::integrate(state,d,dt);
    }
    auto t1=std::chrono::steady_clock::now();
    const double k=runecore::kinetic_energy(state);
    const double p=runecore::potential_energy(state);
    const double e1=k+p;
    auto shaep=runecore::detect_pair_shaeps(state);

    runecore::Metrics m;
    m.count=n;
    m.steps=steps;
    m.dt=dt;
    m.backend="cpu_cpp";
    m.kinetic=k;
    m.potential=p;
    m.total_energy=e1;
    m.energy_drift = e0==0?0:(e1-e0)/std::fabs(e0);
    m.elapsed_ms=std::chrono::duration<double,std::milli>(t1-t0).count();

    runecore::write_state_csv(prefix+"-state.csv",state);
    runecore::write_metrics_json(prefix+"-metrics.json",m,shaep);

    std::cout << "{\"backend\":\"cpu_cpp\",\"count\":"<<n
              <<",\"steps\":"<<steps
              <<",\"elapsed_ms\":"<<m.elapsed_ms
              <<",\"energy_drift\":"<<m.energy_drift
              <<",\"shaep_candidates\":"<<shaep.size()<<"}\n";
}
