#!/bin/env python
"""
Script to check for exact ganglia and httpd package version installed
If not found - install them
If found but version doesn't match - remove and install correct versions
"""
import yum


required_packages = [
    ("httpd", "2.2.29"),
    ("php", "5.3.29"),
    ("ganglia", "3.3.7"),
    ("ganglia-web", "3.3.7"),
    ("ganglia-gmond", "3.3.7"),
    ("ganglia-gmetad", "3.3.7"),
]

yb = yum.YumBase()
installed_packages_dict = dict([(p.name, p) for p in yb.rpmdb.returnPackages()])

operations_log = []

def remove_package(package_name):
    yb.remove(name=package_name)
    yb.resolveDeps()
    yb.buildTransaction()
    yb.processTransaction()


def install_package(package_name, version):
    yb.install(name=package_name, version=version)
    yb.resolveDeps()
    yb.buildTransaction()
    yb.processTransaction()

# uninstall wrong versions
for package_name, required_version in required_packages:
    if package_name in installed_packages_dict:
        installed_package = installed_packages_dict[package_name]
        if not installed_package.version.startswith(required_version):
            print "Removing package: %s %s != %s" % (package_name, installed_package.version, required_version)
            remove_package(package_name)
            operations_log.append("Removed package: %s %s != %s" % (package_name, installed_package.version, required_version))

installed_packages_dict = dict([(p.name, p) for p in yb.rpmdb.returnPackages()])

# install packages
installed_packages_dict = dict([(p.name, p) for p in yb.rpmdb.returnPackages()])
for package_name, required_version in required_packages:
    if package_name not in installed_packages_dict:
        print "installing package %s %s" % (package_name, required_version)
        install_package(package_name, required_version)
        operations_log.append("Installed package: %s %s" % (package_name, required_version))

print "Report:"
if operations_log:
    print "\n".join(operations_log)
else:
    print "All ganglia related packages have been already installed"
