package com.circularcarbon.model;
import jakarta.persistence.*;
import java.util.UUID;
@Entity
@Table(name = "emission_factor", uniqueConstraints = {
    @UniqueConstraint(name = "uk_category_sub_category", columnNames = {"category", "subCategory"})
})
public class EmissionFactor {
    @Id @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    @Enumerated(EnumType.STRING)
    private EmissionCategory category;
    private String subCategory;
    private Double factorValue;
    private String unit;
    private String source;
    
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public EmissionCategory getCategory() { return category; }
    public void setCategory(EmissionCategory category) { this.category = category; }
    public String getSubCategory() { return subCategory; }
    public void setSubCategory(String subCategory) { this.subCategory = subCategory; }
    public Double getFactorValue() { return factorValue; }
    public void setFactorValue(Double factorValue) { this.factorValue = factorValue; }
    public String getUnit() { return unit; }
    public void setUnit(String unit) { this.unit = unit; }
    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }
}
