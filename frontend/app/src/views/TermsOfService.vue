<template>
  <div class="page-container">
    <header class="header">
      <router-link to="/" class="logo-link">
        <div class="logo-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="30" height="30">
            <path fill="#075e54"
              d="M160 368c26.5 0 48 21.5 48 48l0 16 72.5-54.4c8.3-6.2 18.4-9.6 28.8-9.6L448 368c8.8 0 16-7.2 16-16l0-288c0-8.8-7.2-16-16-16L64 48c-8.8 0-16 7.2-16 16l0 288c0 8.8 7.2 16 16 16l96 0zm48 124l-.2 .2-5.1 3.8-17.1 12.8c-4.8 3.6-11.3 4.2-16.8 1.5s-8.8-8.2-8.8-14.3l0-21.3 0-6.4 0-.3 0-4 0-48-48 0-48 0c-35.3 0-64-28.7-64-64L0 64C0 28.7 28.7 0 64 0L448 0c35.3 0 64 28.7 64 64l0 288c0 35.3-28.7 64-64 64l-138.7 0L208 492z" />
          </svg>
        </div>
        <span class="logo-text">WotNot</span>
      </router-link>
    </header>

    <main class="content-wrapper">
      <div class="content-card">
        <h1>Terms of Service</h1>
        <p class="last-updated">Last updated: October 19, 2025</p>

        <section class="section-content">
          <h2>1. Acceptance of Terms</h2>
          <p>
            Welcome to WotNot! These Terms of Service ("Terms") govern your use of the WotNot website and any related services provided by us. By accessing or using our Service, you agree to be bound by these Terms. If you disagree with any part of the terms, then you may not access the Service.
          </p>
        </section>

        <section class="section-content">
          <h2>2. Description of Service</h2>
          <p>
            WotNot is a WhatsApp Business API management platform that allows businesses to:
          </p>
          <ul>
            <li>Send broadcast messages to customers</li>
            <li>Manage customer contacts and groups</li>
            <li>Integrate with e-commerce platforms like WooCommerce</li>
            <li>Analyze messaging performance and customer interactions</li>
            <li>Automate customer communications</li>
          </ul>
        </section>

        <section class="section-content">
          <h2>3. Account Terms</h2>
          <ul>
            <li>You must be at least 18 years old to use this Service</li>
            <li>You are responsible for maintaining the security of your account and password</li>
            <li>You agree to provide true, accurate, current, and complete information when registering for an account</li>
            <li>You may not use the Service for any illegal or unauthorized purpose</li>
            <li>You are responsible for all activities that occur under your account</li>
            <li>You must have a valid WhatsApp Business Account to use our services</li>
          </ul>
        </section>

        <section class="section-content">
          <h2>4. Acceptable Use</h2>
          <p>You agree not to:</p>
          <ul>
            <li>Send spam, unsolicited messages, or violate WhatsApp's policies</li>
            <li>Use the service for illegal activities or to harm others</li>
            <li>Attempt to gain unauthorized access to our systems</li>
            <li>Interfere with or disrupt the service or servers</li>
            <li>Use automated systems to access the service without permission</li>
          </ul>
        </section>

        <section class="section-content">
          <h2>5. WhatsApp Business API Compliance</h2>
          <p>
            By using WotNot, you agree to comply with WhatsApp's Business Policy, Terms of Service, and all applicable guidelines. You are responsible for ensuring that your use of our service complies with these policies.
          </p>
        </section>

        <section class="section-content">
          <h2>6. Intellectual Property</h2>
          <p>
            The Service and its original content, features, and functionality are and will remain the exclusive property of WotNot and its licensors. Our trademarks and trade dress may not be used in connection with any product or service without the prior written consent of WotNot.
          </p>
        </section>

        <section class="section-content">
          <h2>7. Payment Terms</h2>
          <ul>
            <li>Subscription fees are billed in advance on a monthly or annual basis</li>
            <li>All fees are non-refundable unless otherwise stated</li>
            <li>We reserve the right to change our pricing with 30 days notice</li>
            <li>Failure to pay may result in service suspension or termination</li>
          </ul>
        </section>

        <section class="section-content">
          <h2>8. Termination</h2>
          <p>
            We may terminate or suspend your account immediately, without prior notice or liability, for any reason whatsoever, including without limitation if you breach the Terms. Upon termination, your right to use the Service will immediately cease.
          </p>
        </section>

        <section class="section-content">
          <h2>9. Limitation of Liability</h2>
          <p>
            In no event shall WotNot, nor its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, special, consequential, or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your use of the service.
          </p>
        </section>

        <section class="section-content">
          <h2>10. Governing Law</h2>
          <p>
            These Terms shall be governed and construed in accordance with the laws of the United States, without regard to its conflict of law provisions.
          </p>
        </section>

        <section class="section-content">
          <h2>11. Changes to Terms</h2>
          <p>
            We reserve the right, at our sole discretion, to modify or replace these Terms at any time. If a revision is material, we will try to provide at least 30 days notice prior to any new terms taking effect.
          </p>
        </section>

        <section class="section-content">
          <h2>12. Contact Information</h2>
          <p>
            If you have any questions about these Terms of Service, please contact us at:
          </p>
          <ul>
            <li>Email: support@wotnot.com</li>
            <li>Website: https://wotnot.com</li>
          </ul>
        </section>

        <div class="back-link">
          <router-link to="/" class="button">Back to Login</router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "TermsOfService",
};
</script>

<style scoped>
/* Define your color variables based on the WotNot image */
:root {
  --primary-green: #075e54;
  --dark-text: #2d3748;
  --light-grey-background: #f7fafc;
  --border-color: #e2e8f0;
  --shadow-color: rgba(0, 0, 0, 0.08);
  --light-text-color: #6b7280;
}

.page-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--light-grey-background);
  font-family: "Inter", "Helvetica Neue", Arial, sans-serif;
  color: var(--dark-text);
  line-height: 1.7;
  font-size: 16px;
  overflow: hidden;
}

.header {
  padding: 20px 40px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: flex-start;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  flex-shrink: 0;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--dark-text);
}

.logo-icon {
  margin-right: 10px;
}

.logo-text {
  font-weight: 700;
  font-size: 1.5rem;
  color: var(--primary-green);
}

.content-wrapper {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 50px 20px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--primary-green) var(--light-grey-background);
}

.content-wrapper::-webkit-scrollbar {
  width: 8px;
}

.content-wrapper::-webkit-scrollbar-track {
  background: var(--light-grey-background);
  border-radius: 4px;
}

.content-wrapper::-webkit-scrollbar-thumb {
  background-color: var(--primary-green);
  border-radius: 4px;
  border: 2px solid var(--light-grey-background);
}

.content-card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 6px 15px var(--shadow-color);
  border: 1px solid var(--border-color);
  padding: 50px;
  max-width: 850px;
  width: 100%;
  box-sizing: border-box;
}

h1 {
  font-size: 2.5rem;
  color: var(--primary-green);
  margin-bottom: 25px;
  text-align: center;
  border-bottom: 2px solid var(--primary-green);
  padding-bottom: 20px;
  position: relative;
}

h1::after {
  content: "";
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: -2px;
  width: 60px;
  height: 4px;
  background-color: var(--primary-green);
  border-radius: 2px;
}

h2 {
  font-size: 2rem;
  color: var(--dark-text);
  margin-top: 45px;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

p {
  font-size: 1.05rem;
  margin-bottom: 18px;
}

ul {
  list-style-type: disc;
  margin-left: 30px;
  margin-bottom: 20px;
}

li {
  margin-bottom: 10px;
  line-height: 1.7;
}

a {
  color: var(--primary-green);
  text-decoration: none;
  transition: color 0.2s ease-in-out, text-decoration 0.2s ease-in-out;
}

a:hover {
  color: #2f855a;
  text-decoration: underline;
}

.last-updated {
  font-size: 0.95rem;
  color: var(--light-text-color);
  text-align: center;
  margin-bottom: 40px;
}

.back-link {
  margin-top: 50px;
  text-align: center;
}

.button {
  display: inline-block;
  padding: 14px 30px;
  background-color: var(--primary-green);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: background-color 0.2s ease-in-out, transform 0.1s ease-out;
}

.button:hover {
  background-color: #2f855a;
  transform: translateY(-2px);
}

.button:active {
  transform: translateY(0);
}

/* Responsive adjustments for smaller screens */
@media (max-width: 768px) {
  .header {
    padding: 15px 20px;
  }

  .logo-text {
    font-size: 1.3rem;
  }

  .content-wrapper {
    padding: 30px 15px;
  }

  .content-card {
    padding: 30px;
    border-radius: 8px;
  }

  h1 {
    font-size: 2rem;
    margin-bottom: 20px;
    padding-bottom: 15px;
  }

  h1::after {
    width: 40px;
  }

  h2 {
    font-size: 1.6rem;
    margin-top: 35px;
    margin-bottom: 15px;
  }

  p,
  ul,
  li {
    font-size: 1rem;
    margin-bottom: 15px;
  }

  .last-updated {
    margin-bottom: 30px;
  }

  .button {
    padding: 12px 25px;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 10px 15px;
  }

  .logo-text {
    font-size: 1.2rem;
  }

  .content-wrapper {
    padding: 20px 10px;
  }

  .content-card {
    padding: 20px;
  }

  h1 {
    font-size: 1.6rem;
  }

  h2 {
    font-size: 1.3rem;
  }

  p,
  ul,
  li {
    font-size: 0.95rem;
  }
}
</style>
