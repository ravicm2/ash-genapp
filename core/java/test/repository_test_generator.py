# core/java/test_generator/controller_test_generator.py
import os
from utils.logger import get_logger

logger = get_logger(__name__)

def generate_controller_test(app_name, entity):
    class_name = entity['name']
    controller_class_name = f"{class_name}RestController"
    test_class_name = f"{controller_class_name}Test"
    package_path = f"com/ashbyte/{app_name}/controller"
    test_path = f"src/test/java/{package_path}"
    os.makedirs(test_path, exist_ok=True)

    file_path = os.path.join(test_path, f"{test_class_name}.java")

    content = f"""
package {package_path};

import com.ashbyte.{app_name}.dto.{class_name}DTO;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import com.ashbyte.{app_name}.service.{class_name}Service;

import java.util.Collections;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest({controller_class_name}.class)
public class {test_class_name} {{

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private {class_name}Service service;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    public void testCreateEntity() throws Exception {{
        {class_name}DTO dto = new {class_name}DTO();
        mockMvc.perform(post("/api/{class_name.lower()}s")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isOk());
    }}

    @Test
    public void testGetAllEntities() throws Exception {{
        when(service.getAll()).thenReturn(Collections.emptyList());
        mockMvc.perform(get("/api/{class_name.lower()}s"))
                .andExpect(status().isOk());
    }}

    @Test
    public void testGetEntityById() throws Exception {{
        Long id = 1L;
        when(service.getById(id)).thenReturn(new {class_name}DTO());
        mockMvc.perform(get("/api/{class_name.lower()}s/" + id))
                .andExpect(status().isOk());
    }}

    @Test
    public void testUpdateEntity() throws Exception {{
        Long id = 1L;
        {class_name}DTO dto = new {class_name}DTO();
        mockMvc.perform(put("/api/{class_name.lower()}s/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isOk());
    }}

    @Test
    public void testPatchEntity() throws Exception {{
        Long id = 1L;
        {class_name}DTO dto = new {class_name}DTO();
        mockMvc.perform(patch("/api/{class_name.lower()}s/" + id)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isOk());
    }}

    @Test
    public void testDeleteEntity() throws Exception {{
        Long id = 1L;
        doNothing().when(service).deleteById(id);
        mockMvc.perform(delete("/api/{class_name.lower()}s/" + id))
                .andExpect(status().isOk());
    }}

    @Test
    public void testGetEntityById_NotFound() throws Exception {{
        Long id = 99L;
        when(service.getById(id)).thenThrow(new RuntimeException("Entity not found"));
        mockMvc.perform(get("/api/{class_name.lower()}s/" + id))
                .andExpect(status().isInternalServerError());
    }}

    @Test
    public void testCreateEntity_InvalidPayload() throws Exception {{
        String invalidJson = "";
        mockMvc.perform(post("/api/{class_name.lower()}s")
                .contentType(MediaType.APPLICATION_JSON)
                .content(invalidJson))
                .andExpect(status().isBadRequest());
    }}
}}
"""

    with open(file_path, 'w') as f:
        f.write(content)
    logger.info(f"Generated full Controller Test class for {class_name} at {file_path}")