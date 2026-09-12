import os

base_dir = r"c:\Users\Anuj\Desktop\HackOut\circular-carbon\backend"

def write_file(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

write_file("src/main/java/com/circularcarbon/dto/ProcessInputDTO.java", """
package com.circularcarbon.dto;
import java.util.List;
public class ProcessInputDTO {
    private String companyName;
    private String industryType;
    private List<ProcessInputItemDTO> items;
    
    public String getCompanyName() { return companyName; }
    public void setCompanyName(String companyName) { this.companyName = companyName; }
    public String getIndustryType() { return industryType; }
    public void setIndustryType(String industryType) { this.industryType = industryType; }
    public List<ProcessInputItemDTO> getItems() { return items; }
    public void setItems(List<ProcessInputItemDTO> items) { this.items = items; }
}
""")

write_file("src/main/java/com/circularcarbon/dto/ProcessInputItemDTO.java", """
package com.circularcarbon.dto;
import com.circularcarbon.model.EmissionCategory;
public class ProcessInputItemDTO {
    private EmissionCategory category;
    private String itemName;
    private Double quantity;
    private String unit;
    
    public EmissionCategory getCategory() { return category; }
    public void setCategory(EmissionCategory category) { this.category = category; }
    public String getItemName() { return itemName; }
    public void setItemName(String itemName) { this.itemName = itemName; }
    public Double getQuantity() { return quantity; }
    public void setQuantity(Double quantity) { this.quantity = quantity; }
    public String getUnit() { return unit; }
    public void setUnit(String unit) { this.unit = unit; }
}
""")

write_file("src/main/java/com/circularcarbon/dto/EmissionResultDTO.java", """
package com.circularcarbon.dto;
import java.util.List;
public class EmissionResultDTO {
    private Double totalCo2e;
    private List<EmissionBreakdownDTO> breakdowns;
    private List<RecommendationDTO> recommendations;
    
    public Double getTotalCo2e() { return totalCo2e; }
    public void setTotalCo2e(Double totalCo2e) { this.totalCo2e = totalCo2e; }
    public List<EmissionBreakdownDTO> getBreakdowns() { return breakdowns; }
    public void setBreakdowns(List<EmissionBreakdownDTO> breakdowns) { this.breakdowns = breakdowns; }
    public List<RecommendationDTO> getRecommendations() { return recommendations; }
    public void setRecommendations(List<RecommendationDTO> recommendations) { this.recommendations = recommendations; }
}
""")

write_file("src/main/java/com/circularcarbon/dto/EmissionBreakdownDTO.java", """
package com.circularcarbon.dto;
import com.circularcarbon.model.EmissionCategory;
public class EmissionBreakdownDTO {
    private String itemName;
    private EmissionCategory category;
    private Double co2e;
    private Double percentage;
    
    public String getItemName() { return itemName; }
    public void setItemName(String itemName) { this.itemName = itemName; }
    public EmissionCategory getCategory() { return category; }
    public void setCategory(EmissionCategory category) { this.category = category; }
    public Double getCo2e() { return co2e; }
    public void setCo2e(Double co2e) { this.co2e = co2e; }
    public Double getPercentage() { return percentage; }
    public void setPercentage(Double percentage) { this.percentage = percentage; }
}
""")

write_file("src/main/java/com/circularcarbon/dto/RecommendationDTO.java", """
package com.circularcarbon.dto;
import com.fasterxml.jackson.annotation.JsonProperty;
public class RecommendationDTO {
    private String title;
    private String description;
    @JsonProperty("estimated_co2_reduction")
    private String estimatedCo2Reduction;
    @JsonProperty("cost_impact")
    private String costImpact;
    @JsonProperty("implementation_steps")
    private String implementationSteps;
    private String justification;
    
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getEstimatedCo2Reduction() { return estimatedCo2Reduction; }
    public void setEstimatedCo2Reduction(String estimatedCo2Reduction) { this.estimatedCo2Reduction = estimatedCo2Reduction; }
    public String getCostImpact() { return costImpact; }
    public void setCostImpact(String costImpact) { this.costImpact = costImpact; }
    public String getImplementationSteps() { return implementationSteps; }
    public void setImplementationSteps(String implementationSteps) { this.implementationSteps = implementationSteps; }
    public String getJustification() { return justification; }
    public void setJustification(String justification) { this.justification = justification; }
}
""")

write_file("src/main/java/com/circularcarbon/service/EmissionCalculationService.java", """
package com.circularcarbon.service;
import com.circularcarbon.dto.*;
import com.circularcarbon.model.*;
import com.circularcarbon.repository.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.*;

@Service
public class EmissionCalculationService {
    private final EmissionFactorRepository factorRepository;
    private final ProcessInputRepository inputRepository;
    private final EmissionResultRepository resultRepository;
    
    public EmissionCalculationService(EmissionFactorRepository factorRepository, ProcessInputRepository inputRepository, EmissionResultRepository resultRepository) {
        this.factorRepository = factorRepository;
        this.inputRepository = inputRepository;
        this.resultRepository = resultRepository;
    }

    @Transactional
    public EmissionResult calculate(ProcessInputDTO dto) {
        ProcessInput input = new ProcessInput();
        input.setCompanyName(dto.getCompanyName());
        input.setIndustryType(dto.getIndustryType());
        
        List<ProcessInputItem> items = new ArrayList<>();
        double totalCo2e = 0.0;
        List<EmissionBreakdown> breakdowns = new ArrayList<>();
        
        for (ProcessInputItemDTO itemDto : dto.getItems()) {
            ProcessInputItem item = new ProcessInputItem();
            item.setCategory(itemDto.getCategory());
            item.setItemName(itemDto.getItemName());
            item.setQuantity(itemDto.getQuantity());
            item.setUnit(itemDto.getUnit());
            items.add(item);
            
            EmissionFactor factor = factorRepository.findByCategoryAndSubCategory(itemDto.getCategory(), itemDto.getItemName())
                    .orElseThrow(() -> new RuntimeException("Factor not found for " + itemDto.getItemName()));
            
            double co2e = item.getQuantity() * factor.getFactorValue();
            totalCo2e += co2e;
            
            EmissionBreakdown breakdown = new EmissionBreakdown();
            breakdown.setItemName(item.getItemName());
            breakdown.setCategory(item.getCategory());
            breakdown.setQuantity(item.getQuantity());
            breakdown.setFactorValue(factor.getFactorValue());
            breakdown.setCo2e(co2e);
            breakdowns.add(breakdown);
        }
        
        input.setItems(items);
        inputRepository.save(input);
        
        breakdowns.sort((b1, b2) -> Double.compare(b2.getCo2e(), b1.getCo2e()));
        
        for (int i = 0; i < breakdowns.size(); i++) {
            EmissionBreakdown b = breakdowns.get(i);
            b.setRank(i + 1);
            b.setPercentage((b.getCo2e() / totalCo2e) * 100);
        }
        
        EmissionResult result = new EmissionResult();
        result.setProcessInputId(input.getId());
        result.setTotalCo2e(totalCo2e);
        result.setBreakdowns(breakdowns);
        return resultRepository.save(result);
    }
}
""")

write_file("src/main/java/com/circularcarbon/controller/EmissionController.java", """
package com.circularcarbon.controller;
import com.circularcarbon.dto.*;
import com.circularcarbon.model.EmissionResult;
import com.circularcarbon.service.EmissionCalculationService;
import com.circularcarbon.service.RecommendationService;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/emissions")
public class EmissionController {
    private final EmissionCalculationService calcService;
    private final RecommendationService recService;
    
    public EmissionController(EmissionCalculationService calcService, RecommendationService recService) {
        this.calcService = calcService;
        this.recService = recService;
    }

    @PostMapping("/analyze")
    public EmissionResultDTO analyze(@RequestBody ProcessInputDTO request) {
        EmissionResult result = calcService.calculate(request);
        List<RecommendationDTO> recommendations = recService.getRecommendations(request.getCompanyName(), request.getIndustryType(), result);
        
        EmissionResultDTO resDto = new EmissionResultDTO();
        resDto.setTotalCo2e(result.getTotalCo2e());
        
        List<EmissionBreakdownDTO> bdDtos = result.getBreakdowns().stream().map(b -> {
            EmissionBreakdownDTO d = new EmissionBreakdownDTO();
            d.setItemName(b.getItemName());
            d.setCategory(b.getCategory());
            d.setCo2e(b.getCo2e());
            d.setPercentage(b.getPercentage());
            return d;
        }).collect(Collectors.toList());
        
        resDto.setBreakdowns(bdDtos);
        resDto.setRecommendations(recommendations);
        return resDto;
    }
}
""")

write_file("src/main/java/com/circularcarbon/service/RecommendationService.java", """
package com.circularcarbon.service;
import com.circularcarbon.dto.*;
import com.circularcarbon.model.EmissionResult;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class RecommendationService {
    private final RestTemplate restTemplate = new RestTemplate();
    private final String RAG_URL = "http://localhost:8000/api/recommend";

    public List<RecommendationDTO> getRecommendations(String companyName, String industryType, EmissionResult result) {
        Map<String, Object> request = new HashMap<>();
        request.put("company_name", companyName);
        request.put("industry_type", industryType);
        request.put("total_co2e", result.getTotalCo2e());
        
        List<Map<String, Object>> topEmissions = result.getBreakdowns().stream()
                .limit(3)
                .map(b -> {
                    Map<String, Object> map = new HashMap<>();
                    map.put("item_name", b.getItemName());
                    map.put("category", b.getCategory().name());
                    map.put("co2e", b.getCo2e());
                    map.put("percentage", b.getPercentage());
                    return map;
                }).collect(Collectors.toList());
                
        request.put("top_emissions", topEmissions);
        
        try {
            ResponseEntity<RecommendationDTO[]> response = restTemplate.postForEntity(RAG_URL, request, RecommendationDTO[].class);
            if (response.getBody() != null) {
                return Arrays.asList(response.getBody());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return Collections.emptyList();
    }
}
""")

write_file("../data/emission_factors.sql", """
INSERT INTO emission_factor (id, category, sub_category, factor_value, unit, source) VALUES 
(gen_random_uuid(), 'ENERGY', 'Natural Gas', 2.02, 'kg CO2e/kWh', 'DEFRA 2024'),
(gen_random_uuid(), 'ENERGY', 'Grid Electricity', 0.85, 'kg CO2e/kWh', 'DEFRA 2024'),
(gen_random_uuid(), 'ENERGY', 'Coal', 2.93, 'kg CO2e/kg', 'DEFRA 2024'),
(gen_random_uuid(), 'MATERIAL', 'Steel', 1.8, 'kg CO2e/kg', 'EPA GHG'),
(gen_random_uuid(), 'MATERIAL', 'Aluminum', 11.5, 'kg CO2e/kg', 'EPA GHG'),
(gen_random_uuid(), 'MATERIAL', 'Cement', 0.9, 'kg CO2e/kg', 'EPA GHG'),
(gen_random_uuid(), 'WASTE', 'Industrial Waste', 0.45, 'kg CO2e/kg', 'DEFRA 2024'),
(gen_random_uuid(), 'WASTE', 'Plastic Waste', 2.8, 'kg CO2e/kg', 'DEFRA 2024'),
(gen_random_uuid(), 'TRANSPORT', 'Diesel Truck', 2.68, 'kg CO2e/liter', 'DEFRA 2024');
""")

print("Phase 1 logic updated.")
