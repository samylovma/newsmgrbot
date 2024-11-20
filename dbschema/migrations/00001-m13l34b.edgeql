CREATE MIGRATION m13l34bwmcg4scyhvcvt46g7aktnpyohdrgiydkmdloybcvf62jbhq
    ONTO initial
{
  CREATE TYPE default::Source {
      CREATE REQUIRED PROPERTY feed_url: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY health: std::bool;
      CREATE REQUIRED PROPERTY title: std::str;
      CREATE REQUIRED PROPERTY url: std::str;
  };
  CREATE TYPE default::News {
      CREATE REQUIRED LINK source: default::Source;
      CREATE REQUIRED PROPERTY internal_id: std::str;
      CREATE CONSTRAINT std::exclusive ON ((.source, .internal_id));
      CREATE PROPERTY description: std::str;
      CREATE PROPERTY publication_date: std::datetime;
      CREATE REQUIRED PROPERTY title: std::str;
      CREATE REQUIRED PROPERTY url: std::str;
  };
  CREATE TYPE default::User {
      CREATE MULTI LINK subscriptions: default::Source;
      CREATE REQUIRED PROPERTY telegram_id: std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
