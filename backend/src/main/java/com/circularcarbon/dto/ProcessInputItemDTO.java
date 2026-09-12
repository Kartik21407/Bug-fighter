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
