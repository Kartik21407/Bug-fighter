package com.circularcarbon.dto;
import java.util.List;
public class ProcessInputDTO {
    private String companyName;
    private String industryType;
    private List<ProcessInputItemDTO> items;
    
    public String getCompanyName() { return companyName; }
    public void setCompanyName(String companyName) { this.companyName = companyName; }
    public String getIndustryType() { return industryType; }
    public void setIndustryType(String industryType) { this.industryType = industryType; }
    public List<ProcessInputItemDTO> getItems() { return items; }
    public void setItems(List<ProcessInputItemDTO> items) { this.items = items; }
}
