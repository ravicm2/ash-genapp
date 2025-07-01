# repo_generator.py
import os

def to_camel_case(s):
    return ''.join(word.capitalize() for word in s.split('_'))

def generate_repository(entity, base_path, package):
    class_name = to_camel_case(entity['name'])
    package_path = package.replace('.', '/')
    repo_path = os.path.join(base_path, "src", "main", "java", package_path, "repository")
    os.makedirs(repo_path, exist_ok=True)

    repo_code = f"""
package {package}.repository;

import {package}.entity.{class_name};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface {class_name}Repository extends JpaRepository<{class_name}, Long> {{
}}
"""

    with open(os.path.join(repo_path, f"{class_name}Repository.java"), "w") as f:
        f.write(repo_code.strip())