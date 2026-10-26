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
import { articles, contact, data, properties, services } from '../../../data.js';
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
} from '../../../components/index.js';
export function ServicesHeroSection() {
  return (
    <section className="section-top dark">
      <div className="shell">
        <div className="max-w-[850px] mx-auto text-center hero-enter">
          <Heading tag="h1">{'Expert real estate services'}</Heading>
          <p className="muted mt-7">
            {
              'At Naverah Assets, we are proud to be a trusted channel partner for some of the most reputed developers in the industry.'
            }
          </p>
        </div>
        <ServiceGrid />
      </div>
    </section>
  );
}
