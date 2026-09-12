package com.circularcarbon.model;
import jakarta.persistence.*;
import java.util.List;
import java.util.UUID;
import java.time.LocalDateTime;
@Entity
public class ProcessInput {
    @Id @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    private String companyName;
    private String industryType;
    private LocalDateTime createdAt = LocalDateTime.now();
    @OneToMany(cascade = CascadeType.ALL)
    @JoinColumn(name = "process_input_id")
    private List<ProcessInputItem> items;
    
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public String getCompanyName() { return companyName; }
    public void setCompanyName(String companyName) { this.companyName = companyName; }
    public String getIndustryType() { return industryType; }
    public void setIndustryType(String industryType) { this.industryType = industryType; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public List<ProcessInputItem> getItems() { return items; }
    public void setItems(List<ProcessInputItem> items) { this.items = items; }
}
