import os

def to_camel_case(s):
    return ''.join(word.capitalize() for word in s.split('_'))

def generate_dto(entity, base_path, package):
    class_name = to_camel_case(entity['name'])
    package_path = package.replace('.', '/') + "/dto"
    full_path = os.path.join(base_path, "src", "main", "java", package_path)
    os.makedirs(full_path, exist_ok=True)

    imports = set([
        "import lombok.*;",
        "import javax.validation.constraints.*;"
    ])

    def write_dto_file(dto_type, fields):
        dto_name = f"{dto_type}{class_name}DTO"
        lines = [
            f"package {package}.dto;\n",
            f"@Getter",
            f"@Setter",
            f"@Builder",
            f"@NoArgsConstructor",
            f"@AllArgsConstructor",
            f"public class {dto_name} {{"
        ]

        for field in fields:
            annotations = []

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

            ftype = field['type']
            if field.get("relation"):
                ftype = to_camel_case(ftype)
            else:
                ftype = JAVA_TYPE_MAPPING.get(ftype, to_camel_case(ftype))

            for ann in annotations:
                lines.append(f"    {ann}")
            lines.append(f"    private {ftype} {field['name']};\n")

        lines.append("}")

        with open(os.path.join(full_path, f"{dto_name}.java"), "w") as f:
            for imp in sorted(imports):
                f.write(imp + "\n")
            f.write("\n")
            for line in lines:
                f.write(line + "\n")

    # Define which fields go into which DTO type
    entity_fields = entity['fields']
    create_fields = [f for f in entity_fields if not f.get("primary", False)]
    update_fields = entity_fields.copy()
    view_fields = entity_fields.copy()

    write_dto_file("Create", create_fields)
    write_dto_file("Update", update_fields)
    write_dto_file("View", view_fields)


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