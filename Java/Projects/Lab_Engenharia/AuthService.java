package com.example.authservice.service;

import com.example.authservice.dto.AuthenticationRequest;
import com.example.authservice.dto.AuthenticationResponse;
import com.example.authservice.dto.UserDto;
import com.example.authservice.model.User;
import com.example.authservice.repository.UserRepository;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;

import java.time.Instant;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final AuthenticationManager authenticationManager;
    private final UserRepository userRepository;
    private final JwtService jwtService;
    private final TokenBlacklistService tokenBlacklistService;

    // Corresponde a `AuthController->AuthService: authenticate(credentials)`
    public AuthenticationResponse authenticate(AuthenticationRequest request) {
        
        // 1. (AuthService->AuthManager: authenticate)
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        request.email(),
                        request.password()
                )
        );

        // 2. O AuthManager (via UserDetailsService) já validou o usuário.
        //    Buscamos o usuário para obter dados e gerar o token.
        var user = (User) authentication.getPrincipal();

        // 3. (AuthService->JwtService: generateToken)
        var jwtToken = jwtService.generateToken(user);
        
        // 4. (AuthService->JwtService: generateRefreshToken)
        var refreshToken = jwtService.generateRefreshToken(user);

        // 5. (AuthService->UserRepository: updateLastLogin)
        user.setLastLogin(Instant.now());
        userRepository.save(user);
        
        // 6. Monta a resposta
        return new AuthenticationResponse(
                jwtToken,
                refreshToken,
                UserDto.fromEntity(user) // Retorna os dados do usuário
        );
    }

    // Corresponde a `AuthController->TokenBlacklistService: invalidateToken(token)`
    public void logout(HttpServletRequest request) {
        final String authHeader = request.getHeader("Authorization");
        final String jwt;

        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            return; // Nenhuma ação necessária
        }

        jwt = authHeader.substring(7);
        tokenBlacklistService.invalidateToken(jwt);
    }
}