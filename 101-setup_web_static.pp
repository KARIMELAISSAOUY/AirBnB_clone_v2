#!/usr/bin/puppet apply
# AirBnB clone web server setup and configuration

# Update package repositories
exec { 'apt-get-update':
  command => '/usr/bin/apt-get update',
  path    => '/usr/bin:/usr/sbin:/bin',
}

# Remove the current web_static directory
exec { 'remove-current':
  command => 'rm -rf /data/web_static/current',
  path    => '/usr/bin:/usr/sbin:/bin',
}

# Install nginx package
package { 'nginx':
  ensure  => installed,
  require => Exec['apt-get-update'],
}

# Create the /var/www directory
file { '/var/www':
  ensure  => directory,
  mode    => '0755',
  recurse => true,
  require => Package['nginx'],
}

# Create a simple index.html file
file { '/var/www/html/index.html':
  content => 'Hello, World!',
  require => File['/var/www'],
}

# Create a custom 404 error page
file { '/var/www/error/404.html':
  content => "Ceci n'est pas une page",
  require => File['/var/www'],
}

# Create necessary directories for web_static
exec { 'make-static-files-folder':
  command => 'mkdir -p /data/web_static/releases/test /data/web_static/shared',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => Package['nginx'],
}

# Create a custom index.html for the test release
file { '/data/web_static/releases/test/index.html':
  content => "
<!DOCTYPE html>
<html lang='en-US'>
	<head>
		<title>Home - AirBnB Clone</title>
	</head>
	<body>
		<h1>Welcome to AirBnB!</h1>
	</body>
</html>
",
  replace => true,
  require => Exec['make-static-files-folder'],
}

# Link the test release to current
exec { 'link-static-files':
  command => 'ln -sf /data/web_static/releases/test/ /data/web_static/current',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => [
    Exec['remove-current'],
    File['/data/web_static/releases/test/index.html'],
  ],
}

# Change ownership of /data to ubuntu user
exec { 'change-data-owner':
  command => 'chown -hR ubuntu:ubuntu /data',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => Exec['link-static-files'],
}

# Configure Nginx default site
file { '/etc/nginx/sites-available/default':
  ensure  => present,
  mode    => '0644',
  content => "
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	server_name _;
	index index.html index.htm;
	error_page 404 /404.html;
	add_header X-Served-By \$hostname;
	location / {
		root /var/www/html/;
		try_files \$uri \$uri/ =404;
	}
	location /hbnb_static/ {
		alias /data/web_static/current/;
		try_files \$uri \$uri/ =404;
	}
	if (\$request_filename ~ redirect_me){
		rewrite ^ https://sketchfab.com/bluepeno/models permanent;
	}
	location = /404.html {
		root /var/www/error/;
		internal;
	}
}",
  require => [
    Package['nginx'],
    File['/var/www/html/index.html'],
    File['/var/www/error/404.html'],
    Exec['change-data-owner'],
  ],
}

# Enable the default site
exec { 'enable-site':
  command => "ln -sf '/etc/nginx/sites-available/default' '/etc/nginx/sites-enabled/default'",
  path    => '/usr/bin:/usr/sbin:/bin',
  require => File['/etc/nginx/sites-available/default'],
}

# Restart the nginx service
service { 'nginx':
  ensure     => 'running',
  enable     => true,
  subscribe  => Exec['enable-site'],
  require    => [
    Exec['change-data-owner'],
    Package['nginx'],
    File['/data/web_static/releases/test/index.html'],
  ],
}
