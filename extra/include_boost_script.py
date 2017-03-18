import operator

s1 = "#include <boost/"
lines1 = {}
with open('./boost_includes_1') as f:
	lines=f.readlines()
	for line in lines:
		if s1 in line:
			line1 = line[line.find('#'):line.find('\n')]
			if lines1.has_key(line1):
				lines1[line1] = lines1[line1] + 1
			else:
				lines1[line1]=1;
	sorted_x = sorted(lines1.items(), key=operator.itemgetter(1))
	for line in sorted_x:
		print line
f.close()

'''

sed scripts to remove some boost deps:

make_shared:
find . -type f -not -path '*/\.*' -exec sed -i 's/boost::make_shared/std::make_shared/g' {} +
find . -type f -not -path '*/\.*' -exec sed -i 's/#include <boost\/make_shared.hpp>/#include <memory>/g' {} +

shared_ptr:
find . -type f -not -path '*/\.*' -exec sed -i 's/std::shared_ptr/std::shared_ptr/g' {} +
find . -type f -not -path '*/\.*' -exec sed -i 's/#include <boost\/shared_ptr.hpp>/#include <memory>/g' {} +

bind:
find . -type f -not -path '*/\.*' -exec sed -i 's/boost::bind/std::bind/g' {} +
find . -type f -not -path '*/\.*' -exec sed -i 's/#include <boost\/bind.hpp>/#include <functional>/g' {} +

function:
find . -type f -not -path '*/\.*' -exec sed -i 's/boost::function/std::function/g' {} +
find . -type f -not -path '*/\.*' -exec sed -i 's/#include <boost\/function.hpp>/#include <functional>/g' {} +

scoped_ptr
find . -type f -not -path '*/\.*' -exec sed -i 's/boost::scoped_ptr/std::unique_ptr/g' {} +
find . -type f -not -path '*/\.*' -exec sed -i 's/#include <boost\/scoped_ptr.hpp>/#include <memory>/g' {} +

To remove:
<boost/math/special_functions/fpclassify.hpp>: marketmodel.cpp, matrices.cpp, simulatedannealing.cpp
change to <cmath>
change boost::math::isnan to std::isnan and boost::math::isinf to std::isinf
script:
	find . -type f -not -path '*/\.*' -not -path '*/extra' -exec sed -i 's/boost::math::isnan/std::isnan/g' {} +
	find . -type f -not -path '*/\.*' -not -path '*/extra' -exec sed -i 's/boost::math::isinf/std::isinf/g' {} +
	find */marketmodel.cpp */matrices.cpp */*/*/simulatedannealing.hpp -type f -not -path '*/\.*' -not -path '*/extra' -exec sed -i 's/#include <boost\/math\/special_functions\/fpclassify.hpp>/#include <cmath>/g' {} +

Other math/special_functions also similar:
gamma.hpp = not replacable - only gaama_q and gamma_q_inv in noarbsabr.cpp
atanh.hpp:
	find . -type f -not -path '*/\.*' -exec sed -i 's/boost::math::atanh/std::atanh/g' {} +
	find blackformula.cpp -type f -not -path '*/\.*' -exec sed -i 's/#include <boost\/math\/special_functions\/atanh.hpp>/#include <cmath>/g' {} +
erf.hpp
	find */*/*/*/gaussian1dmodel.cpp -type f -not -path '*/\.*' -not -path '*/extra' -exec sed -i 's/boost::math::erf/std::erf/g' {} +
	find */*/*/*/gaussian1dmodel.hpp -type f -not -path '*/\.*' -not -path '*/extra' -exec sed -i 's/#include <boost\/math\/special_functions\/erf.hpp>/#include <cmath>/g' {} +

---

boost/atomic:
	find observable.hpp observable.cpp singleton.hpp -type f -not -path '*/\.*' -not -path '*/extra' -exec sed -i 's/boost::atomic/std::atomic/g' {} +
	find observable.hpp observable.cpp singleton.hpp -type f -not -path '*/\.*' -not -path '*/extra' -exec sed -i 's/#include <boost\/math\/special_functions\/erf.hpp>/#include <cmath>/g' {} +



boost/random

not doing for lambda as non-polymorphic only maybe
not doing for thread at present



'''