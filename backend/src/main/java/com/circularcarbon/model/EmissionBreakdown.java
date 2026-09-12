package com.circularcarbon.model;
import jakarta.persistence.*;
import java.util.UUID;
@Entity
public class EmissionBreakdown {
    @Id @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    private String itemName;
    @Enumerated(EnumType.STRING)
    private EmissionCategory category;
    private Double quantity;
    private Double factorValue;
    private Double co2e;
    private Integer rank;
    private Double percentage;
    
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public String getItemName() { return itemName; }
    public void setItemName(String itemName) { this.itemName = itemName; }
    public EmissionCategory getCategory() { return category; }
    public void setCategory(EmissionCategory category) { this.category = category; }
    public Double getQuantity() { return quantity; }
    public void setQuantity(Double quantity) { this.quantity = quantity; }
    public Double getFactorValue() { return factorValue; }
    public void setFactorValue(Double factorValue) { this.factorValue = factorValue; }
    public Double getCo2e() { return co2e; }
    public void setCo2e(Double co2e) { this.co2e = co2e; }
    public Integer getRank() { return rank; }
    public void setRank(Integer rank) { this.rank = rank; }
    public Double getPercentage() { return percentage; }
    public void setPercentage(Double percentage) { this.percentage = percentage; }
}
