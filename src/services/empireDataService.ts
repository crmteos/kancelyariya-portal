// Empire Data Service - Chancery Ukrainian Imperial Portal
// Provides functions for loading and managing JSON data files

// ============================================================
// CORE ENTITY SERVICE
// ============================================================

export interface EntityCore {
  entity_id: string;
  region_name_ua: string;
  synonyms_ua: string[];
  synonyms_ru: string[];
  media_directive?: string | null;
}

export interface EntityCoreLoader {
  (): Promise<EntityCore[]>;
}

// Load all core entities from JSON
export const loadEntitiesCore: EntityCoreLoader = async (): Promise<EntityCore[]> => {
  const response = await fetch('/src/data/core/entities_core.json');
  return response.json();
};

// ============================================================
// CHANCERY DIRECTIVE SERVICE
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

export interface ChanceryDirectiveLoader {
  (): Promise<ChanceryDirective[]>;
}

// Load all chancery directives from JSON
export const loadChanceryDirectives: ChanceryDirectiveLoader = async (): Promise<ChanceryDirective[]> => {
  const response = await fetch('/src/data/modules/chancery_directives.json');
  return response.json();
};

// ============================================================
// PORTAL LAYOUT SERVICE
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

export interface PortalLayoutLoader {
  (): Promise<PortalLayout[]>;
}

// Load all portal layouts from JSON
export const loadPortalLayout: PortalLayoutLoader = async (): Promise<PortalLayout[]> => {
  const response = await fetch('/src/data/modules/portal_layout.json');
  return response.json();
};

// ============================================================
// MEDIA CAMPAIGN SERVICE
// ============================================================

export interface MediaCampaign {
  entity_id: string;
  region_name_ua: string;
  synonyms_ua: string[];
  synonyms_ru: string[];
  media_directive?: string | null;
}

export interface MediaCampaignLoader {
  (): Promise<MediaCampaign[]>;
}

// Load all media campaigns from JSON
export const loadMediaCampaigns: MediaCampaignLoader = async (): Promise<MediaCampaign[]> => {
  const response = await fetch('/src/data/modules/media_campaigns.json');
  return response.json();
};

// ============================================================
// UTILITY FUNCTIONS
// ============================================================

// Get entity by ID across all data sources
export const findEntityById = (
  id: string,
  entities: EntityCore[],
  directives: ChanceryDirective[],
  layouts: PortalLayout[],
  campaigns: MediaCampaign[]
) => ({
  core: entities.find(e => e.entity_id === id),
  directive: directives.find(d => d.entity_id === id),
  layout: layouts.find(l => l.entity_id === id),
  campaign: campaigns.find(c => c.entity_id === id),
});

// Get region code info by entity ID
export const getRegionInfo = (entityId: string): RegionCode => {
  const regionMap: Record<string, RegionCode> = {
    'UA-01': { code: 'UA-01', name_ua: 'Автономна Республіка Крим', name_ru: 'Автономная Республика Крым', synonyms_ua: ['АРК', 'Крим', 'Таврида'], synonyms_ru: ['АРК', 'Крым', 'Таврида'] },
    'UA-02': { code: 'UA-02', name_ua: 'Вінницька область', name_ru: 'Винницкая область', synonyms_ua: ['Вінниччина', 'Поділля'], synonyms_ru: ['Винничина', 'Подолье'] },
    // Additional mappings can be generated from the JSON data
  };
  return regionMap[entityId] || { code: entityId, name_ua: '', name_ru: '', synonyms_ua: [], synonyms_ru: [] };
};

// Get all media campaigns for a region
export const getCampaignsByRegion = (entityId: string, campaigns: MediaCampaign[]): MediaCampaign[] => {
  return campaigns.filter(campaign => campaign.entity_id === entityId);
};

// Initialize all data services
export const initializeDataServices = async (): Promise<{
  entities: EntityCore[];
  directives: ChanceryDirective[];
  layouts: PortalLayout[];
  campaigns: MediaCampaign[];
}> => {
  const [entities, directives, layouts, campaigns] = await Promise.all([
    loadEntitiesCore(),
    loadChanceryDirectives(),
    loadPortalLayout(),
    loadMediaCampaigns(),
  ]);
  
  return { entities, directives, layouts, campaigns };
};
export interface OsintPassport {
  id: string;
  country: string;
  code: string;
  region: string;
  fields: string[];
}

export interface OsintPassportLoader {
  (): Promise<OsintPassport[]>;
}

// Load all OSINT passports from JSON
export const loadOsintPassports: OsintPassportLoader = async (): Promise<OsintPassport[]> => {
  const response = await fetch('/src/data/modules/regional_passports_master.json');
  const data = await response.json();
  return data.passports;
}

// Initialize all data services
export const initializeDataServices = async (): Promise<{
  entities: EntityCore[];
  directives: ChanceryDirective[];
  layouts: PortalLayout[];
  campaigns: MediaCampaign[];
  passports: OsintPassport[];
}> => {
  const [entities, directives, layouts, campaigns, passports] = await Promise.all([
    loadEntitiesCore(),
    loadChanceryDirectives(),
    loadPortalLayout(),
    loadMediaCampaigns(),
    loadOsintPassports(),
  ]);

  return { entities, directives, layouts, campaigns, passports };
};
// Get full profile combining core entity data with OSINT passport
export const getEntityFullProfile = (entityId: string, entities: EntityCore[], passports: OsintPassport[]) => {
  const coreEntity = entities.find(e => e.entity_id === entityId);
  const passport = passports.find(p => p.id === entityId || p.code === entityId);
  
  if (!coreEntity) {
    return null;
  }
  
  return {
    ...coreEntity,
    ...(passport ? { osint_passport: passport } : {}),
  };
};
