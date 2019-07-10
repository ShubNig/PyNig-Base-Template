#!/usr/bin/env bash

pip_install_requires_list=(
    requests>=2.21.0
    faker>=1.0.1
)
pip_install_test_requirements_list=(
    mock>=2.0.0
)

pV(){
    echo -e "\033[;36m$1\033[0m"
}
pI(){
    echo -e "\033[;32m$1\033[0m"
}
pD(){
    echo -e "\033[;34m$1\033[0m"
}
pW(){
    echo -e "\033[;33m$1\033[0m"
}
pE(){
    echo -e "\033[;31m$1\033[0m"
}

checkFuncBack(){
    if [ $? -ne 0 ]; then
        echo -e "\033[;31mRun [ $1 ] error exit code 1\033[0m"
        exit 1
        # else
        #   echo -e "\033[;30mRun [ $1 ] success\033[0m"
    fi
}

checkEnv(){
    evn_checker=`which $1`
    checkFuncBack "which $1"
    if [ ! -n "evn_checker" ]; then
        echo -e "\033[;31mCheck event [ $1 ] error exit\033[0m"
        exit 1
        # else
        #   echo -e "\033[;32mCli [ $1 ] event check success\033[0m\n-> \033[;34m$1 at Path: ${evn_checker}\033[0m"
    fi
}

checkUserAsRoot(){
    if [[ "$USER" != "root" ]]; then
        echo -e "\033[;31mMust run as root\033[0m"
        exit 1
    fi
}

checkEnv python
python -V
checkEnv pip
pip -V

for pip_pkg in ${pip_install_requires_list[@]};
do
  pV "Install requirement package ${pip_pkg} use pip"
  python -m pip install ${pip_pkg}
  checkFuncBack "python -m pip install ${pip_pkg}"
done
exit 0

for pip_pkg in ${pip_install_test_requirements_list[@]};
do
  pV "Install test requirement package ${pip_pkg} use pip"
  python -m pip install ${pip_pkg}
  checkFuncBack "python -m pip install ${pip_pkg}"
done



