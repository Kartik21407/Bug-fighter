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
