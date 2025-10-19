<template>
  <div class="page-container">
    <header class="header">
      <div class="header-content">
        <router-link to="/" class="logo-link">
          <div class="logo-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="32" height="32">
              <path fill="#075e54"
                d="M160 368c26.5 0 48 21.5 48 48l0 16 72.5-54.4c8.3-6.2 18.4-9.6 28.8-9.6L448 368c8.8 0 16-7.2 16-16l0-288c0-8.8-7.2-16-16-16L64 48c-8.8 0-16 7.2-16 16l0 288c0 8.8 7.2 16 16 16l96 0zm48 124l-.2 .2-5.1 3.8-17.1 12.8c-4.8 3.6-11.3 4.2-16.8 1.5s-8.8-8.2-8.8-14.3l0-21.3 0-6.4 0-.3 0-4 0-48-48 0-48 0c-35.3 0-64-28.7-64-64L0 64C0 28.7 28.7 0 64 0L448 0c35.3 0 64 28.7 64 64l0 288c0 35.3-28.7 64-64 64l-138.7 0L208 492z" />
            </svg>
          </div>
          <span class="logo-text">WotNot</span>
        </router-link>
        
        <!-- Quick Navigation -->
        <nav class="header-nav">
          <router-link to="/terms-of-service" class="nav-link">Terms of Service</router-link>
          <router-link to="/" class="nav-link primary">Back to Login</router-link>
        </nav>
      </div>
    </header>

    <main class="content-wrapper">
      <div class="content-card">
        <h1>Privacy Policy</h1>
        <p class="last-updated">Last updated: October 19, 2025</p>

        <section class="section-content">
          <h2>1. Introduction</h2>
          <p>
            Your privacy is important to us. This Privacy Policy describes how WotNot ("we," "us," or "our") collects, uses, and discloses your personal information when you use our website and WhatsApp Business API management platform (the "Service").
          </p>
        </section>

        <section class="section-content">
          <h2>2. Information We Collect</h2>
          
          <div class="data-categories">
            <div class="data-category">
              <div class="category-icon">👤</div>
              <h3>Account Information</h3>
              <p>When you register for an account, we collect:</p>
              <ul>
                <li>Email address</li>
                <li>Business name</li>
                <li>Password (stored securely as a hash)</li>
                <li>Contact preferences</li>
              </ul>
            </div>

            <div class="data-category">
              <div class="category-icon">📱</div>
              <h3>WhatsApp Business Data</h3>
              <p>To provide our services, we collect:</p>
              <ul>
                <li>WhatsApp Business Account ID (WABA ID)</li>
                <li>Phone Number ID</li>
                <li>Permanent Access Token (encrypted and stored securely)</li>
                <li>Message templates and content</li>
                <li>Customer phone numbers (for messaging)</li>
              </ul>
            </div>

            <div class="data-category">
              <div class="category-icon">📊</div>
              <h3>Usage Analytics</h3>
              <p>We automatically collect:</p>
              <ul>
                <li>Message delivery status and metrics</li>
                <li>Customer interaction data</li>
                <li>Platform usage statistics</li>
                <li>Error logs and performance data</li>
              </ul>
            </div>
          </div>

          <h3>Usage Data:</h3>
          <p>
            We may also collect information that your browser sends whenever you visit our Service ("Usage Data"). This Usage Data may include information such as:
          </p>
          <ul>
            <li>Your computer's Internet Protocol address (IP address)</li>
            <li>Browser type and version</li>
            <li>The pages of our Service that you visit</li>
            <li>The time and date of your visit</li>
            <li>The time spent on those pages</li>
            <li>Unique device identifiers</li>
            <li>Other diagnostic data</li>
          </ul>

          <h3>WhatsApp Data:</h3>
          <p>
            Through your WhatsApp Business Account integration, we may process:
          </p>
          <ul>
            <li>Contact information from your WhatsApp Business contacts</li>
            <li>Message content and metadata (as permitted by WhatsApp policies)</li>
            <li>Customer interaction data</li>
            <li>Broadcast campaign performance metrics</li>
          </ul>
        </section>

        <section class="section-content">
          <h2>3. How We Use Your Information</h2>
          <p>WotNot uses the collected data for various purposes:</p>
          <ul>
            <li>To provide and maintain the Service</li>
            <li>To notify you about changes to our Service</li>
            <li>To allow you to participate in interactive features of our Service when you choose to do so</li>
            <li>To provide customer support</li>
            <li>To monitor the usage of the Service</li>
            <li>To detect, prevent, and address technical issues</li>
            <li>To process WhatsApp Business API requests</li>
            <li>To manage broadcast campaigns and customer communications</li>
            <li>To provide analytics and reporting on messaging performance</li>
          </ul>
        </section>

        <section class="section-content">
          <h2>4. Data Storage and Security</h2>
          <p>
            We implement appropriate technical and organizational security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction. Your data is stored securely using industry-standard encryption.
          </p>
          <ul>
            <li>Passwords are hashed using secure algorithms</li>
            <li>Access tokens are encrypted and stored securely</li>
            <li>All data transmission is encrypted using HTTPS</li>
            <li>Regular security audits and updates</li>
            <li>Limited access to personal data on a need-to-know basis</li>
          </ul>
        </section>

        <section class="section-content">
          <h2>5. Data Sharing and Disclosure</h2>
          <p>
            We may share your information with trusted third parties who assist us in operating our website, conducting our business, or serving our users, so long as those parties agree to keep this information confidential. We may also release your information when we believe release is appropriate to comply with the law, enforce our site policies, or protect ours or others' rights, property, or safety.
          </p>
          
          <h3>Third-Party Services:</h3>
          <ul>
            <li><strong>WhatsApp/Meta:</strong> We integrate with WhatsApp Business API as per their terms and policies</li>
            <li><strong>WooCommerce:</strong> For e-commerce integration features</li>
            <li><strong>Cloud Hosting Providers:</strong> For secure data storage and processing</li>
            <li><strong>Analytics Services:</strong> For service improvement and performance monitoring</li>
          </ul>
        </section>

        <section class="section-content">
          <h2>6. Data Retention</h2>
          <p>
            We retain your personal information for as long as necessary to provide our services and comply with legal obligations. Specifically:
          </p>
          <ul>
            <li>Account information is retained while your account is active</li>
            <li>Usage data is typically retained for 24 months</li>
            <li>WhatsApp data is retained according to WhatsApp's policies</li>
            <li>We may retain certain data longer for legal compliance or security purposes</li>
          </ul>
        </section>

        <section class="section-content">
          <h2>7. Your Data Protection Rights</h2>
          <p>
            Depending on your location, you may have the following data protection rights:
          </p>
          <ul>
            <li><strong>Access:</strong> The right to access, update, or delete the information we have on you</li>
            <li><strong>Rectification:</strong> The right to correct inaccurate personal information</li>
            <li><strong>Erasure:</strong> The right to request deletion of your personal data</li>
            <li><strong>Portability:</strong> The right to receive your data in a structured format</li>
            <li><strong>Objection:</strong> The right to object to processing of your personal data</li>
            <li><strong>Restriction:</strong> The right to request restriction of processing</li>
            <li><strong>Withdrawal of Consent:</strong> The right to withdraw consent at any time</li>
          </ul>
          <p>
            To exercise any of these rights, please contact us at privacy@wotnot.com.
          </p>
        </section>

        <section class="section-content">
          <h2>8. Cookies and Tracking</h2>
          <p>
            We use cookies and similar tracking technologies to enhance your experience on our Service. You can control cookie preferences through your browser settings.
          </p>
        </section>

        <section class="section-content">
          <h2>9. International Data Transfers</h2>
          <p>
            Your information may be transferred to and processed in countries other than your own. We ensure appropriate safeguards are in place for such transfers in accordance with applicable data protection laws.
          </p>
        </section>

        <section class="section-content">
          <h2>10. Children's Privacy</h2>
          <p>
            Our Service is not intended for children under 18 years of age. We do not knowingly collect personal information from children under 18.
          </p>
        </section>

        <section class="section-content">
          <h2>11. Changes to This Privacy Policy</h2>
          <p>
            We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the "Last updated" date. You are advised to review this Privacy Policy periodically for any changes.
          </p>
        </section>

        <section class="section-content">
          <h2>12. Contact Information</h2>
          <p>
            If you have any questions about this Privacy Policy, please contact us at:
          </p>
          <ul>
            <li>Email: privacy@wotnot.com</li>
            <li>General Support: support@wotnot.com</li>
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
  name: "PrivacyPolicy",
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
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  flex-shrink: 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--dark-text);
  transition: transform 0.2s ease;
}

.logo-link:hover {
  transform: scale(1.02);
}

.logo-icon {
  margin-right: 12px;
}

.logo-text {
  font-weight: 700;
  font-size: 1.6rem;
  color: var(--primary-green);
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  text-decoration: none;
  color: var(--dark-text);
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background-color: var(--light-grey-background);
  color: var(--primary-green);
}

.nav-link.primary {
  background-color: var(--primary-green);
  color: white;
}

.nav-link.primary:hover {
  background-color: #2f855a;
  transform: translateY(-1px);
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

h3 {
  font-size: 1.5rem;
  color: var(--dark-text);
  margin-top: 30px;
  margin-bottom: 15px;
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

  h3 {
    font-size: 1.3rem;
    margin-top: 25px;
    margin-bottom: 10px;
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

  h3 {
    font-size: 1.1rem;
  }

  p,
  ul,
  li {
    font-size: 0.95rem;
  }
}

/* Data Categories */
.data-categories {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
  margin: 30px 0;
}

.data-category {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 1px solid #0ea5e9;
  border-radius: 12px;
  padding: 24px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.data-category::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #0ea5e9, #0284c7);
}

.data-category:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(14, 165, 233, 0.15);
}

.category-icon {
  font-size: 2.5rem;
  margin-bottom: 16px;
  text-align: center;
}

.data-category h3 {
  color: #0284c7;
  font-weight: 600;
  margin: 0 0 12px 0;
  font-size: 1.2rem;
  text-align: center;
}

.data-category p {
  margin: 0 0 16px 0;
  color: #0369a1;
  font-weight: 500;
  text-align: center;
}

.data-category ul {
  margin: 0;
  padding-left: 20px;
}

.data-category li {
  color: #0c4a6e;
  margin-bottom: 8px;
  font-size: 0.95rem;
}
</style>
