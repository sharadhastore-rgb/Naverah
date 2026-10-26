import { useState } from 'react';
import {
  ArrowDown,
  ArrowUpRight,
  Building2,
  Check,
  HeartHandshake,
  Lightbulb,
  Mail,
  MapPin,
  Phone,
  Search,
  ShieldCheck,
  Users,
} from 'lucide-react';
import { articles, contact, data, properties, services } from '../../data.js';
import {
  BlogCard,
  Button,
  ContactForm,
  CTA,
  FAQ,
  Gallery,
  Heading,
  Office,
  Pagination,
  Picture,
  PropertyCard,
  ServiceGrid,
  TeamGrid,
} from '../../components/index.js';
import { ServicesHeroSection } from './sections/ServicesHeroSection.js';
import { PropertyTypesSection } from './sections/PropertyTypesSection.js';
import { FaqSection } from './sections/FaqSection.js';
export function ServicesPage() {
  return (
    <>
      <ServicesHeroSection />
      <PropertyTypesSection />
      <FaqSection />
    </>
  );
}
