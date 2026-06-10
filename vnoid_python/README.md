
# test vnoid

```
git clone https://github.com/choreonoid/choreonoid.git

cd choreonoid

(cd ext; git clone https://github.com/IRSL-tut/vnoid.git -b vnoid_python)

mkdir -p choreonoid/build

cd build

cmake .. -DCMAKE_INSTALL_PREFIX=/tmp/cnoid

make -j$(nproc)

make -j$(nproc) install

cd /tmp/cnoid

bin/choreonoid share/choreonoid-2.5/project/vnoid_sample_project.cnoid
```

# test python

see test.py
