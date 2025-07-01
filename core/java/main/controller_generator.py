# controller_generator.py
import os

def to_camel_case(s):
    return ''.join(word.capitalize() for word in s.split('_'))

def to_snake_case(name):
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def generate_controller(entity, base_path, package):
    class_name = to_camel_case(entity['name'])
    var_name = class_name[0].lower() + class_name[1:]
    base_url = f"/api/{to_snake_case(entity['name'])}"

    package_path = package.replace('.', '/')
    controller_path = os.path.join(base_path, "src", "main", "java", package_path, "controller")
    os.makedirs(controller_path, exist_ok=True)

    controller_code = f"""
package {package}.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import {package}.service.{class_name}Service;
import {package}.dto.*;
import jakarta.validation.Valid;

@RestController
@RequestMapping("{base_url}")
public class {class_name}Controller {{

    @Autowired
    private {class_name}Service service;

    @PostMapping
    public ResponseEntity<{class_name}DTO> create(@Valid @RequestBody Create{class_name}DTO dto) {{
        return ResponseEntity.ok(service.create(dto));
    }}

    @GetMapping("/{{id}}")
    public ResponseEntity<{class_name}DTO> getById(@PathVariable Long id) {{
        return ResponseEntity.ok(service.getById(id));
    }}

    @GetMapping
    public ResponseEntity<Page<{class_name}DTO>> getAll(Pageable pageable) {{
        return ResponseEntity.ok(service.getAll(pageable));
    }}

    @PutMapping("/{{id}}")
    public ResponseEntity<{class_name}DTO> update(@PathVariable Long id, @Valid @RequestBody Update{class_name}DTO dto) {{
        return ResponseEntity.ok(service.update(id, dto));
    }}

    @PatchMapping("/{{id}}")
    public ResponseEntity<{class_name}DTO> partialUpdate(@PathVariable Long id, @RequestBody Update{class_name}DTO dto) {{
        return ResponseEntity.ok(service.update(id, dto)); // Reuse update for patch
    }}

    @DeleteMapping("/{{id}}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {{
        service.delete(id);
        return ResponseEntity.noContent().build();
    }}

    // Flexible pattern match example. This is just for an example. Kindly remove when not required.
    // @GetMapping("/users/{{userId}}/department/{{deptId}}")
    // public ResponseEntity<String> getUserDept(@PathVariable Long userId, @PathVariable Long deptId) {{
    //    return ResponseEntity.ok("User: " + userId + ", Department: " + deptId);
    // }}
}}
"""

    with open(os.path.join(controller_path, f"{class_name}Controller.java"), "w") as f:
        f.write(controller_code.strip())