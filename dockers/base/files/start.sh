cd ${PROJECT_ROOT}/lab
#npm install
webpack --watch &
pm2 start lab.config.js --watch
bash