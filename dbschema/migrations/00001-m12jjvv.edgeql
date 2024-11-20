CREATE MIGRATION m12jjvvqbeqri2wz6wqvvffn2v75hqd4oot7jhw3xd7ijb5vi2dgda
    ONTO initial
{
  CREATE ABSTRACT TYPE default::Auditable {
      CREATE REQUIRED PROPERTY created_at: std::datetime {
          SET readonly := true;
          CREATE REWRITE
              INSERT 
              USING (std::datetime_of_statement());
      };
      CREATE REQUIRED PROPERTY updated_at: std::datetime {
          SET readonly := true;
          CREATE REWRITE
              INSERT 
              USING (std::datetime_of_statement());
          CREATE REWRITE
              UPDATE 
              USING (std::datetime_of_statement());
      };
  };
  CREATE TYPE default::Source EXTENDING default::Auditable {
      CREATE REQUIRED PROPERTY feed_url: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY health: std::bool;
      CREATE REQUIRED PROPERTY title: std::str;
      CREATE REQUIRED PROPERTY url: std::str;
  };
  CREATE TYPE default::News EXTENDING default::Auditable {
      CREATE REQUIRED LINK source: default::Source;
      CREATE REQUIRED PROPERTY internal_id: std::str;
      CREATE CONSTRAINT std::exclusive ON ((.source, .internal_id));
      CREATE PROPERTY description: std::str;
      CREATE PROPERTY publication_date: std::datetime;
      CREATE REQUIRED PROPERTY title: std::str;
      CREATE REQUIRED PROPERTY url: std::str;
  };
  CREATE TYPE default::User EXTENDING default::Auditable {
      CREATE MULTI LINK subscriptions: default::Source;
      CREATE REQUIRED PROPERTY telegram_id: std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
