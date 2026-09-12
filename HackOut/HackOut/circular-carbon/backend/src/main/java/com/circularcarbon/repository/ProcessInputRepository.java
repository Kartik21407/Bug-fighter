package com.circularcarbon.repository;
import com.circularcarbon.model.ProcessInput;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;
public interface ProcessInputRepository extends JpaRepository<ProcessInput, UUID> { }
