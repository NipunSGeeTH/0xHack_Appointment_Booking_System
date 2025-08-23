<template>
  <div>
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">Welcome to Sri Lankan Government Services Portal</h1>
          <p class="hero-subtitle">
            Streamline your government service experience. Book appointments, submit documents, 
            and manage your visits online with ease and convenience.
          </p>
          <div class="hero-actions">
            <router-link to="/services" class="btn btn-primary btn-lg">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
              Explore Services
            </router-link>
            <router-link to="/book" class="btn btn-outline btn-lg">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
              Book Appointment
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="container">
        <div class="section-header">
          <h2>Why Choose Our Portal?</h2>
          <p>Experience government services like never before with our modern, efficient platform.</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="feature-card">
            <div class="feature-icon">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h3>24/7 Availability</h3>
            <p>Access government services anytime, anywhere. No more waiting in long queues or rushing to offices during business hours.</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h3>Secure & Reliable</h3>
            <p>Your data is protected with state-of-the-art security measures. Government-grade encryption ensures your privacy.</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
            <h3>Fast & Efficient</h3>
            <p>Complete your government transactions in minutes, not hours. Streamlined processes save you time and effort.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Services Preview -->
    <section class="services-preview">
      <div class="container">
        <div class="section-header">
          <h2>Popular Services</h2>
          <p>Quick access to the most commonly used government services.</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="service-card">
            <div class="service-icon">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
            <h4>Birth Certificate</h4>
            <p>Apply for birth certificates and related documents.</p>
          </div>
          
          <div class="service-card">
            <div class="service-icon">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <h4>Passport Services</h4>
            <p>Renew or apply for new passports online.</p>
          </div>
          
          <div class="service-card">
            <div class="service-icon">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
              </svg>
            </div>
            <h4>Property Registration</h4>
            <p>Register properties and land documents.</p>
          </div>
          
          <div class="service-card">
            <div class="service-icon">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <h4>Tax Services</h4>
            <p>File taxes and manage tax-related documents.</p>
          </div>
        </div>
        
        <div class="text-center mt-8">
          <router-link to="/services" class="btn btn-outline">
            View All Services
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>


