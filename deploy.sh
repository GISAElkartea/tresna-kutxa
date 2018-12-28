#!/usr/bin/env bash

ssh -T www@biltokia.joxemizumalabe.eus <<'END'
cd tresna-kutxa
git pull origin master
sudo nixos-rebuild switch
for command in 'collectstatic --noinput' migrate compilemessages buildwatson; do
     nix-shell nix --run "python manage.py ${command} --settings=tk.production"
done
# systemctl restart uwsgi
END
