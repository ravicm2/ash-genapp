# exception_generator.py
import os

def generate_exception_classes(base_path, package):
    package_path = package.replace('.', '/')
    exception_path = os.path.join(base_path, "src", "main", "java", package_path, "exception")
    os.makedirs(exception_path, exist_ok=True)

    exception_classes = {
        "GlobalExceptionHandler": f"""
package {package}.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;
import java.util.HashMap;
import java.util.Map;

@ControllerAdvice
public class GlobalExceptionHandler {{

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<Object> handleResourceNotFound(ResourceNotFoundException ex, WebRequest request) {{
        return new ResponseEntity<>(createError(ex.getMessage()), HttpStatus.NOT_FOUND);
    }}

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Object> handleValidationErrors(MethodArgumentNotValidException ex) {{
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error ->
            errors.put(error.getField(), error.getDefaultMessage())
        );
        return new ResponseEntity<>(errors, HttpStatus.BAD_REQUEST);
    }}

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Object> handleGeneric(Exception ex) {{
        return new ResponseEntity<>(createError("Internal Server Error"), HttpStatus.INTERNAL_SERVER_ERROR);
    }}

    private Map<String, String> createError(String message) {{
        Map<String, String> error = new HashMap<>();
        error.put("error", message);
        return error;
    }}
}}
""",
        "ResourceNotFoundException": f"""
package {package}.exception;

public class ResourceNotFoundException extends RuntimeException {{
    public ResourceNotFoundException(String message) {{
        super(message);
    }}
}}
"""
    }

    for filename, content in exception_classes.items():
        with open(os.path.join(exception_path, f"{filename}.java"), "w") as f:
            f.write(content.strip())