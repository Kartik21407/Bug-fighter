package com.circularcarbon.service;
import com.circularcarbon.dto.*;
import com.circularcarbon.model.EmissionResult;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.ResponseEntity;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class RecommendationService {
    private final RestTemplate restTemplate = new RestTemplate();
    
    @Value("${rag.service.url:http://localhost:8000/api/recommend}")
    private String ragUrl;

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
            ResponseEntity<RecommendationDTO[]> response = restTemplate.postForEntity(ragUrl, request, RecommendationDTO[].class);
            if (response.getBody() != null) {
                return Arrays.asList(response.getBody());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return Collections.emptyList();
    }
}
