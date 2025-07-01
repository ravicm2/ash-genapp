# service_generator.py
import os

def to_camel_case(s):
    return ''.join(word.capitalize() for word in s.split('_'))

def generate_service_interface(entity, base_path, package):
    class_name = to_camel_case(entity['name'])
    package_path = package.replace('.', '/')
    service_path = os.path.join(base_path, "src", "main", "java", package_path, "service")
    os.makedirs(service_path, exist_ok=True)

    interface_code = f"""
package {package}.service;

import java.util.List;
import {package}.dto.*;

public interface {class_name}Service {{
    {class_name}DTO create(Create{class_name}DTO dto);
    {class_name}DTO update(Long id, Update{class_name}DTO dto);
    void delete(Long id);
    {class_name}DTO getById(Long id);
    List<{class_name}DTO> getAll();
}}
"""

    with open(os.path.join(service_path, f"{class_name}Service.java"), "w") as f:
        f.write(interface_code.strip())

def generate_service_impl(entity, base_path, package):
    class_name = to_camel_case(entity['name'])
    package_path = package.replace('.', '/')
    service_path = os.path.join(base_path, "src", "main", "java", package_path, "service")

    impl_code = f"""
package {package}.service;

import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;

import {package}.repository.{class_name}Repository;
import {package}.dto.*;
import {package}.entity.{class_name};

@Service
public class {class_name}ServiceImpl implements {class_name}Service {{

    @Autowired
    private {class_name}Repository repository;

    private {class_name} toEntity(Create{class_name}DTO dto) {{
        {class_name} entity = new {class_name}();
        // TODO: set fields manually from dto to entity
        return entity;
    }}

    private {class_name}DTO toDTO({class_name} entity) {{
        {class_name}DTO dto = new {class_name}DTO();
        // TODO: set fields manually from entity to dto
        return dto;
    }}

    @Override
    public {class_name}DTO create(Create{class_name}DTO dto) {{
        {class_name} entity = toEntity(dto);
        entity = repository.save(entity);
        return toDTO(entity);
    }}

    @Override
    public {class_name}DTO update(Long id, Update{class_name}DTO dto) {{
        {class_name} entity = repository.findById(id).orElseThrow();
        // TODO: update entity fields from dto
        entity = repository.save(entity);
        return toDTO(entity);
    }}

    @Override
    public void delete(Long id) {{
        repository.deleteById(id);
    }}

    @Override
    public {class_name}DTO getById(Long id) {{
        return toDTO(repository.findById(id).orElseThrow());
    }}

    @Override
    public List<{class_name}DTO> getAll() {{
        return repository.findAll()
                         .stream()
                         .map(this::toDTO)
                         .collect(Collectors.toList());
    }}
}}
"""

    with open(os.path.join(service_path, f"{class_name}ServiceImpl.java"), "w") as f:
        f.write(impl_code.strip())