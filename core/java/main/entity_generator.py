import os

JAVA_TYPE_MAPPING = {
    "string": "String",
    "int": "int",
    "long": "Long",
    "float": "Float",
    "double": "Double",
    "boolean": "Boolean",
    "date": "LocalDate",
    "datetime": "LocalDateTime"
}

VALIDATION_ANNOTATIONS = {
    "notNull": "@NotNull",
    "email": "@Email",
    "min": "@Min({value})",
    "max": "@Max({value})",
    "size": "@Size(min = {min}, max = {max})"
}

RELATION_ANNOTATIONS = {
    "oneToOne": "@OneToOne",
    "oneToMany": "@OneToMany",
    "manyToOne": "@ManyToOne",
    "manyToMany": "@ManyToMany"
}

def to_camel_case(s):
    return ''.join(word.capitalize() for word in s.split('_'))

def generate_entity(entity, base_path, package):
    class_name = to_camel_case(entity['name'])
    package_path = package.replace('.', '/') + f"/{entity['name'].lower()}"
    full_path = os.path.join(base_path, "src", "main", "java", package_path)
    os.makedirs(full_path, exist_ok=True)

    imports = set([
        "import javax.persistence.*;",
        "import java.io.Serializable;",
        "import lombok.*;",
        "import javax.validation.constraints.*;"
    ])

    lines = [
        f"package {package}.{entity['name'].lower()};\n",
        "@Entity",
        "@Table(name = \"{}\")".format(entity['name'].lower()),
        "@Getter",
        "@Setter",
        "@Builder",
        "@NoArgsConstructor",
        "@AllArgsConstructor",
        f"public class {class_name} implements Serializable {{"
    ]

    for field in entity['fields']:
        annotations = []
        ftype = field['type']
        fname = field['name']

        # Primary Key
        if field.get("primary", False):
            annotations.append("@Id")
            annotations.append("@GeneratedValue(strategy = GenerationType.IDENTITY)")

        # Validation
        if not field.get("nullable", True):
            annotations.append("@NotNull")

        if field.get("email"):
            annotations.append("@Email")

        if field.get("min"):
            annotations.append(f"@Min({field['min']})")

        if field.get("max"):
            annotations.append(f"@Max({field['max']})")

        if field.get("minLength") or field.get("maxLength"):
            min_len = field.get("minLength", 0)
            max_len = field.get("maxLength", 255)
            annotations.append(f"@Size(min = {min_len}, max = {max_len})")

        # Relationship
        if field.get("relation"):
            rel_type = field["relation"]
            annotations.append(RELATION_ANNOTATIONS[rel_type])
            if rel_type in ["manyToOne", "oneToOne"]:
                annotations.append(f"@JoinColumn(name = \"{fname}_id\")")
            elif rel_type in ["oneToMany", "manyToMany"] and field.get("mappedBy"):
                annotations[-1] = f"{RELATION_ANNOTATIONS[rel_type]}(mappedBy = \"{field['mappedBy']}\")"
            if rel_type in ["oneToMany", "manyToMany"]:
                ftype = f"List<{to_camel_case(ftype)}>"
                imports.add("import java.util.List;")
            else:
                ftype = to_camel_case(ftype)
        else:
            ftype = JAVA_TYPE_MAPPING.get(ftype, to_camel_case(ftype))

        # Column
        if not field.get("relation"):
            annotations.append(f"@Column(name = \"{fname}\", nullable = {str(field.get('nullable', True)).lower()})")

        for ann in annotations:
            lines.append(f"    {ann}")
        lines.append(f"    private {ftype} {fname};\n")

    lines.append("}")

    with open(os.path.join(full_path, f"{class_name}.java"), "w") as f:
        for imp in sorted(imports):
            f.write(imp + "\n")
        f.write("\n")
        for line in lines:
            f.write(line + "\n")