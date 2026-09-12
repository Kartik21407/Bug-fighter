import os

base_dir = r"c:\Users\Anuj\Desktop\HackOut\circular-carbon\backend"

def write_file(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

write_file("src/main/java/com/circularcarbon/model/EmissionFactor.java", """
package com.circularcarbon.model;
import jakarta.persistence.*;
import java.util.UUID;
@Entity
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
""")

write_file("src/main/java/com/circularcarbon/model/ProcessInput.java", """
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
""")

write_file("src/main/java/com/circularcarbon/model/ProcessInputItem.java", """
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
""")

write_file("src/main/java/com/circularcarbon/model/EmissionResult.java", """
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
""")

write_file("src/main/java/com/circularcarbon/model/EmissionBreakdown.java", """
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
""")

write_file("src/main/java/com/circularcarbon/repository/EmissionFactorRepository.java", """
package com.circularcarbon.repository;
import com.circularcarbon.model.EmissionFactor;
import com.circularcarbon.model.EmissionCategory;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;
import java.util.UUID;
public interface EmissionFactorRepository extends JpaRepository<EmissionFactor, UUID> {
    Optional<EmissionFactor> findByCategoryAndSubCategory(EmissionCategory category, String subCategory);
}
""")

write_file("src/main/java/com/circularcarbon/repository/ProcessInputRepository.java", """
package com.circularcarbon.repository;
import com.circularcarbon.model.ProcessInput;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;
public interface ProcessInputRepository extends JpaRepository<ProcessInput, UUID> { }
""")

write_file("src/main/java/com/circularcarbon/repository/EmissionResultRepository.java", """
package com.circularcarbon.repository;
import com.circularcarbon.model.EmissionResult;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;
public interface EmissionResultRepository extends JpaRepository<EmissionResult, UUID> { }
""")

print("Phase 1 entities generated.")
