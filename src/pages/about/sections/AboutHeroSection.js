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
export function AboutHeroSection() {
  return (
    <section className="about-top dark">
      <div className="shell">
        <div className="section-head hero-enter">
          <Heading tag="h1" line>
            {'Your trusted partner in property'}
          </Heading>
          <div className="flex gap-5 flex-wrap shrink-0">
            <Button light />
            <Button href="#our-story" outline light arrow={false}>
              {'Our story'}
            </Button>
          </div>
        </div>
        <div className="about-images">
          <Picture
            src={data.images.founder}
            alt="Naveed Ahmed Shaikh"
            className="hero-enter"
            eager
          />
          <Picture src={data.images.about} alt="Naverah Assets" className="hero-enter" eager />
        </div>
      </div>
    </section>
  );
}
