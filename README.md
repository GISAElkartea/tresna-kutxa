
# Requirements

You should a PostgreSQL >= 9 running locally, with a user `biltokia` with access
to a database `biltokia`. The user should be able to authenticate without a
password.

To setup this in NixOS:

    services.postgresql.enable = true;
    services.postgresql.package = pkgs.postgresql_10;
    services.postgresql.authentication = ''
      # Generated file; do not edit!
      local all all                trust
      host  all all 127.0.0.1/32   trust
      host  all all ::1/128        trust
    '';
    services.postgresql.initialScript = pkgs.writeText "init" ''
      CREATE USER biltokia SUPERUSER;
      CREATE DATABASE biltokia OWNER biltokia;
    '';

If this is not your setup, then you will have to fiddle with `DATABASE` in
`tk/settings.py`.

# Installing dependencies

Using Nix:

    nix-shell nix

If you want to use Python 3's virtual envs, you will first have to create one:

    python3 -m venv .

Then activate it:

    source bin/activate

And install the dependencies:

    pip install -r requirements.txt

# Common commands
    
Run any pending database migrations:

    python manage.py migrate

Create a superuser:

    python manage.py createsuperuser

Run the thing:

    python manage.py runserver
