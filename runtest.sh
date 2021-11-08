# su -m $SUDO_USER <<'EOF'
#   if [ ! -d "work" ]; then
#     mkdir -p workspace
#     cd workspace
#     git clone git@github.com:terminal-labs/bash-environment-templates
#     cd ..
#   fi
#   if [ ! -d "utils" ]; then
#     mkdir -p utils
#     cd utils
#     wget https://tl-toolbelt.s3.us-west-2.amazonaws.com/toolbelt-0.1.0.pex
#     cd ..
#   fi
# EOF

sudo chmod +x utils/toolbelt-0.1.0.pex
./utils/toolbelt-0.1.0.pex scan.py
