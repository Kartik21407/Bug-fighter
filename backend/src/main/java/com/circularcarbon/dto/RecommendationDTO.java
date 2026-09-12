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
