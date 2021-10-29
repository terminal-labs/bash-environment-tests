su -m $SUDO_USER <<'EOF'
  if [ ! -d "work" ]; then
    mkdir -p workspace
    cd workspace
    git clone git@github.com:terminal-labs/bash-environment-templates
    cd ..
  fi
  if [ ! -d "utils" ]; then
    mkdir -p utils
    cd utils
    wget https://tl-toolbelt.s3.us-west-2.amazonaws.com/toolbelt-0.1.0.pex
    cd ..
  fi
EOF
cd workspace
cd bash-environment-templates
cd samples

echo "bimodel flavor"
echo "##################"
cd bimodal
ls
echo ""
cd ..

echo "conda flavor"
echo "##################"
cd conda
ls
echo ""
cd ..

echo "ondesktop flavor"
echo "##################"
cd ondesktop
ls
echo ""
cd ..

echo "onguest flavor"
echo "##################"
cd onguest
ls
echo ""
cd ..

echo "onhost flavor"
echo "##################"
cd onhost
ls
echo ""
cd ..

echo "salt flavor"
echo "##################"
cd salt
ls
echo ""
cd ..

# cd conda
# cd python
# su -m $SUDO_USER <<'EOF'
#    sudo make vagrant.conda
# EOF
cd ../../..
sudo chmod +x utils/toolbelt-0.1.0.pex
./utils/toolbelt-0.1.0.pex scan.py
