package com.circularcarbon.repository;
import com.circularcarbon.model.EmissionResult;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;
public interface EmissionResultRepository extends JpaRepository<EmissionResult, UUID> { }
