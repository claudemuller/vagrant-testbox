class webserver {
  exec { 'apt-update':
    command => '/usr/bin/apt-get update'
  }

  # Apache
  package { 'apache':
    name      => 'apache2',
    ensure    => 'installed',
    require   => Exec['apt-update'],
  }

  file { 'site-config':
    path    => '/etc/apache2/sites-available/temp.local.conf',
    source  => '/vagrant/files/apache/temp.local.conf',
    require => Package['apache'],
  }

  # PHPMyAdmin
  package { 'phpmyadmin':
    name   => 'phpmyadmin',
    ensure => 'installed',
  }

  # PHP
  package { 'php':
    name    => 'php5',
    ensure  => 'installed',
  }

  package { 'php-mcrypt':
    name    => 'php5-mcrypt',
    ensure  => 'installed',
    require => Package['php'],
  }

  package { 'php-mysql':
    name    => 'php5-mysql',
    ensure  => 'installed',
    require => Package['php', 'mysql'],
  }

  # MySQL
  package { 'mysql':
    name    => 'mysql-server',
    ensure  => 'installed',
  }
  exec { 'set_mysql_root_password':
    subscribe => [Package['mysql-server']],
    unless    => 'mysqladmin -uroot -proot status',
    path      => '/bin:/usr/bin',
    command   => 'mysqladmin -uroot password root',
  }

  # a2enmod
  exec { 'enable_mod_rewrite':
    subscribe => [Package['apache']],
    path      => '/usr/sbin/:/usr/bin/',
    command   => 'a2enmod rewrite',
  }

  # Exim4
  package { 'exim4':
    name    => 'exim4-daemon-light',
    ensure  => 'installed',
  }

  # Vim
  package { 'vim':
    name   => 'vim',
    ensure => 'installed',
  }
}

class restart_services {
  # Service(s) restart
  service { 'apache':
    name        => 'apache2',
    ensure      => 'running',
    hasrestart  => true,
    # subscribe   => File['site-config'],
    require     => Package['apache'],
  }

  service { 'mysql':
    ensure      => 'running',
    hasrestart  => true,
    require     => Package['mysql'],
  }
}

include webserver
include restart_services
