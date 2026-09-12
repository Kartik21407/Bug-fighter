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
