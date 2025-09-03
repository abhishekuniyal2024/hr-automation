#!/usr/bin/env python3
"""
Test script to demonstrate INR salary conversion
"""

def calculate_salary_range_inr(current_salary_usd: float) -> str:
    """
    Calculate appropriate salary range for the new position in INR
    """
    # Convert USD to INR (approximate rate: 1 USD = 83 INR)
    usd_to_inr_rate = 83
    
    # Convert current salary from USD to INR
    current_salary_inr = current_salary_usd * usd_to_inr_rate
    
    # Adjust salary based on market conditions (5-15% increase)
    min_salary_inr = current_salary_inr * 1.05
    max_salary_inr = current_salary_inr * 1.15
    
    return f"₹{min_salary_inr:,.0f} - ₹{max_salary_inr:,.0f}"

def main():
    print("💰 Salary Conversion: USD to INR")
    print("=" * 50)
    
    # Test with the Senior Software Engineer salary from employees.csv
    original_salary_usd = 90000.0
    
    print(f"Original Salary (USD): ${original_salary_usd:,.2f}")
    print(f"USD to INR Rate: 1 USD = ₹83")
    print(f"Original Salary (INR): ₹{original_salary_usd * 83:,.2f}")
    print()
    
    # Calculate new salary range in INR
    salary_range_inr = calculate_salary_range_inr(original_salary_usd)
    print(f"New Salary Range (INR): {salary_range_inr}")
    print()
    
    # Show the breakdown
    min_salary_inr = original_salary_usd * 83 * 1.05
    max_salary_inr = original_salary_usd * 83 * 1.15
    
    print("Breakdown:")
    print(f"  Minimum: ₹{min_salary_inr:,.2f} (5% increase)")
    print(f"  Maximum: ₹{max_salary_inr:,.2f} (15% increase)")
    print()
    
    # Show what the LinkedIn-style posting would look like
    print("🚀 Sample LinkedIn-Style Job Posting with INR Salary:")
    print("=" * 60)
    print(f"""🚀 **Senior Software Engineer** - Join Our Growing Engineering Team!

💰 Salary Range: {salary_range_inr}
⏰ Experience: 5+ years

---

## 🎯 What Makes This Role Exciting?

We're looking for a passionate **Senior Software Engineer** who's ready to make a real impact in our Engineering department. This isn't just another job – you'll be part of a dynamic team building innovative solutions!

### 🌟 Why You'll Love Working With Us:
• Innovation-Driven Culture: Work on cutting-edge technologies
• Growth Opportunities: Clear path for career advancement
• Impact: Your work will directly improve our products and services
• Collaboration: Join a team of talented professionals

---

## 🔧 What You'll Be Doing:

• Lead key initiatives and contribute to strategic projects
• Collaborate with cross-functional teams to deliver high-quality solutions
• Develop and implement best practices and processes
• Mentor junior team members and share knowledge
• Stay updated with industry trends and emerging technologies
• Contribute to continuous improvement efforts

---

## 🎯 What We're Looking For:

### Required Skills:
• 5+ years of relevant experience
• Strong technical and analytical skills
• Excellent communication and collaboration abilities
• Problem-solving mindset and attention to detail
• Ability to work in a fast-paced environment

### Bonus Points:
• Experience with modern tools and technologies
• Leadership or mentoring experience
• Industry certifications or advanced education
• Track record of successful project delivery

---

## 🎁 What's In It For You:

• Competitive compensation with performance bonuses
• Health and wellness benefits
• Professional development opportunities
• Flexible work arrangements
• Collaborative team environment
• Work-life balance focus

---

## 🚀 Ready to Make an Impact?

If you're excited about joining a dynamic team where your contributions matter, we'd love to hear from you!

**Apply now** and let's build something amazing together! 🚀

---

#hiring #engineering #seniorsoftwareengineer #careers #jobopportunity""")

if __name__ == "__main__":
    main()
