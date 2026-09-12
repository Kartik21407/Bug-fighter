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
