package com.circularcarbon.model;
import jakarta.persistence.*;
import java.util.UUID;
@Entity
public class ProcessInputItem {
    @Id @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    @Enumerated(EnumType.STRING)
    private EmissionCategory category;
    private String itemName;
    private Double quantity;
    private String unit;
    
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public EmissionCategory getCategory() { return category; }
    public void setCategory(EmissionCategory category) { this.category = category; }
    public String getItemName() { return itemName; }
    public void setItemName(String itemName) { this.itemName = itemName; }
    public Double getQuantity() { return quantity; }
    public void setQuantity(Double quantity) { this.quantity = quantity; }
    public String getUnit() { return unit; }
    public void setUnit(String unit) { this.unit = unit; }
}
