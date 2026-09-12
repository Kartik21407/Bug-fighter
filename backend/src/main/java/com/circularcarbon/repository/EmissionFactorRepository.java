package com.circularcarbon.repository;
import com.circularcarbon.model.EmissionFactor;
import com.circularcarbon.model.EmissionCategory;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;
import java.util.UUID;
public interface EmissionFactorRepository extends JpaRepository<EmissionFactor, UUID> {
    Optional<EmissionFactor> findFirstByCategoryAndSubCategory(EmissionCategory category, String subCategory);
}
