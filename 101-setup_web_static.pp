# web_server_setup.pp

# Install Nginx package
package { 'nginx':
  ensure => installed,
}

# Create directory structure
file { '/data':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

file { '/data/web_static':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

file { '/data/web_static/releases':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

file { '/data/web_static/shared':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

file { '/data/web_static/releases/test':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html><body>This is a test HTML file</body></html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  force  => true,
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
    }

    location / {
        try_files \$uri \$uri/ =404;
    }
}
",
  notify => Service['nginx'],
}

# Ensure Nginx service is running and enable on boot
service { 'nginx':
  ensure => running,
  enable => true,
}
