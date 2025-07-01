# core/java/test_generator/service_test_generator.py
import os
from utils.logger import get_logger

logger = get_logger(__name__)

def generate_service_test(app_name, entity):
    class_name = entity['name']
    service_class_name = f"{class_name}Service"
    test_class_name = f"{service_class_name}Test"
    package_path = f"com/ashbyte/{app_name}/service"
    test_path = f"src/test/java/{package_path}"
    os.makedirs(test_path, exist_ok=True)

    file_path = os.path.join(test_path, f"{test_class_name}.java")

    content = f"""
package {package_path};

import com.ashbyte.{app_name}.entity.{class_name};
import com.ashbyte.{app_name}.repository.{class_name}Repository;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

public class {test_class_name} {{

    @Mock
    private {class_name}Repository {class_name.lower()}Repository;

    @InjectMocks
    private {service_class_name} {class_name.lower()}Service;

    private {class_name} sample{class_name};

    @BeforeEach
    void setUp() {{
        MockitoAnnotations.openMocks(this);
        sample{class_name} = new {class_name}();
        sample{class_name}.setId(1L);
        // Add more field initializations as needed
    }}

    @Test
    void testCreate{class_name}() {{
        when({class_name.lower()}Repository.save(any({class_name}.class))).thenReturn(sample{class_name});
        {class_name} created = {class_name.lower()}Service.create{class_name}(sample{class_name});
        assertNotNull(created);
        assertEquals(sample{class_name}.getId(), created.getId());
    }}

    @Test
    void testGet{class_name}ById() {{
        when({class_name.lower()}Repository.findById(1L)).thenReturn(Optional.of(sample{class_name}));
        Optional<{class_name}> found = {class_name.lower()}Service.get{class_name}ById(1L);
        assertTrue(found.isPresent());
        assertEquals(1L, found.get().getId());
    }}

    @Test
    void testUpdate{class_name}() {{
        when({class_name.lower()}Repository.findById(1L)).thenReturn(Optional.of(sample{class_name}));
        when({class_name.lower()}Repository.save(any({class_name}.class))).thenReturn(sample{class_name});
        {class_name} updated = {class_name.lower()}Service.update{class_name}(1L, sample{class_name});
        assertNotNull(updated);
        assertEquals(1L, updated.getId());
    }}

    @Test
    void testDelete{class_name}() {{
        doNothing().when({class_name.lower()}Repository).deleteById(1L);
        {class_name.lower()}Service.delete{class_name}(1L);
        verify({class_name.lower()}Repository, times(1)).deleteById(1L);
    }}
}}
"""

    with open(file_path, 'w') as f:
        f.write(content)
    logger.info(f"Generated Service Test class for {class_name} at {file_path}")