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
export function StorySection() {
  return (
    <section id="our-story" className="section">
      <div className="shell">
        <div className="split-story">
          <div className="reveal">
            <Heading>{'More than a real estate firm'}</Heading>
            <p className="muted mt-7">{data.about[0]}</p>
            <div className="mt-8">
              <Button />
            </div>
          </div>
          <Picture src={properties[5].image} alt={properties[5].title} className="reveal" />
        </div>
        <div className="split-story section pb-0">
          <Picture src={data.images.mission} alt="Our mission" className="reveal" />
          <div className="reveal">
            <Heading>{'A meaningful journey of growth'}</Heading>
            <p className="muted mt-7">{data.about[1]}</p>
            <p className="muted mt-7">
              {
                'To provide clients with trusted, insightful, and personalized real estate guidance. To deliver sustainable, long-term value in every transaction and relationship.'
              }
            </p>
            <div className="mt-8">
              <Button href="#our-values" outline arrow={false}>
                {'Our values'}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
