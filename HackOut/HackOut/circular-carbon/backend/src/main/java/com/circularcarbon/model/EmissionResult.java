package com.circularcarbon.model;
import jakarta.persistence.*;
import java.util.List;
import java.util.UUID;
import java.time.LocalDateTime;
@Entity
public class EmissionResult {
    @Id @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    private UUID processInputId;
    private Double totalCo2e;
    private LocalDateTime calculatedAt = LocalDateTime.now();
    @OneToMany(cascade = CascadeType.ALL)
    @JoinColumn(name = "result_id")
    private List<EmissionBreakdown> breakdowns;
    
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public UUID getProcessInputId() { return processInputId; }
    public void setProcessInputId(UUID processInputId) { this.processInputId = processInputId; }
    public Double getTotalCo2e() { return totalCo2e; }
    public void setTotalCo2e(Double totalCo2e) { this.totalCo2e = totalCo2e; }
    public LocalDateTime getCalculatedAt() { return calculatedAt; }
    public void setCalculatedAt(LocalDateTime calculatedAt) { this.calculatedAt = calculatedAt; }
    public List<EmissionBreakdown> getBreakdowns() { return breakdowns; }
    public void setBreakdowns(List<EmissionBreakdown> breakdowns) { this.breakdowns = breakdowns; }
}
