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
            
            EmissionFactor factor = factorRepository.findFirstByCategoryAndSubCategory(itemDto.getCategory(), itemDto.getItemName())
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
