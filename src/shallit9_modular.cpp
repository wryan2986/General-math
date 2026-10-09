#include <cstdint>
#include <iostream>
#include <vector>
#include <cstdlib>
#include <chrono>
#include <string>
using u64=uint64_t;
using u128=__uint128_t;
constexpr u64 P=(1ULL<<61)-1;
u64 add(u64 a,u64 b){u64 t=a+b; return t>=P?t-P:t;}
u64 sub(u64 a,u64 b){return a>=b?a-b:a+P-b;}
u64 mul(u64 a,u64 b){u128 t=u128(a)*b;u64 r=(u64(t)&P)+u64(t>>61);return r>=P?r-P:r;}
u64 power(u64 a,u64 n){u64 r=1;for(;n;n>>=1,a=mul(a,a))if(n&1)r=mul(r,a);return r;}
int main(int argc,char**argv){
 size_t length=argc>1?std::stoull(argv[1]):8192;
 size_t max_order=argc>2?std::stoull(argv[2]):length/2;
 bool dump=argc>3 && std::string(argv[3])=="dump";
 std::vector<u64>a{1};
 constexpr int morphism[5][2]={{0,0},{1,2},{2,3},{1,4},{3,2}};
 while(a.size()<length){std::vector<u64>b;b.reserve(2*a.size());for(auto x:a){b.push_back(morphism[x][0]);b.push_back(morphism[x][1]);}a.swap(b);}
 a.resize(length);
 if(dump)for(size_t k=0;k<a.size();k++)std::cout<<"D 1 "<<k<<" "<<a[k]<<"\n";
 std::vector<u64>older(length+2,1),prev=a,cur,products;
 auto start=std::chrono::steady_clock::now();u64 checked=length;
 for(size_t n=2;n<=max_order && 2*n-1<=length;n++){
  size_t count=length-2*n+2;cur.resize(count);products.resize(count+1);products[0]=1;
  for(size_t k=0;k<count;k++){
   if(older[k+2]==0){std::cerr<<"Unexpected zero divisor order="<<n-2<<" shift="<<k+2<<"\n";return 3;}
   products[k+1]=mul(products[k],older[k+2]);
  }
  u64 inv=power(products[count],P-2);
  for(size_t k=count;k-->0;){
   u64 q=mul(inv,products[k]);inv=mul(inv,older[k+2]);
   cur[k]=mul(sub(mul(prev[k],prev[k+2]),mul(prev[k+1],prev[k+1])),q);
   if(dump)std::cout<<"D "<<n<<" "<<k<<" "<<cur[k]<<"\n";
   if(cur[k]==0){std::cout<<"ZERO order="<<n<<" shift="<<k<<" prefix="<<length<<" prime="<<P<<"\n";return 2;}
  }
  checked+=count;older.swap(prev);prev.swap(cur);
  if(n%256==0){double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();std::cerr<<"order="<<n<<" checked="<<checked<<" elapsed_seconds="<<sec<<"\n";}
 }
 double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
 std::cout<<"NONZERO prefix="<<length<<" max_order="<<max_order<<" checked="<<checked<<" prime="<<P<<" elapsed_seconds="<<sec<<"\n";
}
