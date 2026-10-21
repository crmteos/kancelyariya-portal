// Empire Data Types - Chancery Ukrainian Imperial Portal
// Generated from: chancery_manifest.json, media_campaigns.json,
//                 entities_core.json, chancery_directives.json, portal_layout.json

// ============================================================
// CORE ENTITY TYPES
// ============================================================

export interface RegionCode {
  code: string;
  name_ua: string;
  name_ru: string;
  synonyms_ua: string[];
  synonyms_ru: string[];
}

export interface EntityCore {
  entity_id: string;
  region_name_ua: string;
  synonyms_ua: string[];
  synonyms_ru: string[];
  media_directive?: string | null;
}

// ============================================================
// CHANCERY DIRECTIVE TYPES
// ============================================================

export interface ChanceryDirective {
  entity_id: string;
  region_name: string;
  status: string;
  governance_body?: string | null;
  security_mode?: string | null;
  demilitarization_level: string;
  resource_quota_pct?: number | null;
  chancery_directive?: string | null;
}

// ============================================================
// MEDIA CAMPAIGN TYPES
// ============================================================

export interface MediaCampaign {
  entity_id: string;
  region_name_ua: string;
  synonyms_ua: string[];
  synonyms_ru: string[];
  media_directive?: string | null;
}

// ============================================================
// PORTAL LAYOUT TYPES
// ============================================================

export interface PortalLayout {
  entity_id: string;
  display_name_ua: string;
  display_name_ru: string;
  capital_ua: string;
  status: string;
  ui_card_color: string;
  widgets: string[];
  portal_directive?: string | null;
}

// ============================================================
// DATA HUB / SCHEMA REGISTRY TYPES
// ============================================================

export interface Contour {
  name: string;
  ukrainian: string;
  description: string;
  language: string;
}

export interface WorkerNode {
  name: string;
  role: string;
  memory: string;
  primary_registry?: string;
  primary_key?: string;
  google_maps_mid?: string;
  sub_agents?: string[];
}

export interface Coordinates {
  lat: number;
  lng: number;
  map_layer_id: string;
}

export interface OsintProfile {
  infrastructure_status: string;
  smotryaschy_nickname: string;
  social_tension: string;
  operational_signals: string[];
}

export interface OsintPassportSchema {
  region_code: number;
  original_name: string;
  imperial_title: string;
  assigned_ataman: string;
  contour: string;
  coordinates: Coordinates;
  osint_profile: OsintProfile;
}

export interface DataHubManifest {
  data_hub: string;
  contours: Contour[];
  worker_nodes: WorkerNode[];
  media_categories: string[];
  osint_passport_schema: OsintPassportSchema;
  osint_profile: OsintProfile;
}

// ============================================================
// MEDIA CATEGORIES ENUM
// ============================================================

export const MediaCategories: readonly string[] = [
  'Історія',
  'Новини',
  'Футуризм'
] as const;

export type MediaCategory = typeof MediaCategories[number];
