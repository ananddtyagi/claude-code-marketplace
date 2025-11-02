#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

/**
 * Script to remove invalid "agents" field from plugin.json manifests
 *
 * The "agents" field causes plugin loading failures because Claude Code
 * automatically discovers the agents/ directory without needing this field.
 */

function findPluginJsonFiles(dir) {
  const results = [];
  const items = fs.readdirSync(dir, { withFileTypes: true });

  for (const item of items) {
    if (!item.isDirectory()) continue;

    const pluginDir = path.join(dir, item.name);
    const manifestPath = path.join(pluginDir, '.claude-plugin', 'plugin.json');

    if (fs.existsSync(manifestPath)) {
      results.push({
        name: item.name,
        path: manifestPath
      });
    }
  }

  return results;
}

async function fixPluginManifests() {
  console.log('Finding all plugin.json files...');

  const pluginsDir = path.resolve(__dirname, '..', 'plugins');
  const pluginFiles = findPluginJsonFiles(pluginsDir);

  console.log(`Found ${pluginFiles.length} plugin.json files\n`);

  let fixedCount = 0;
  let skippedCount = 0;
  let errorCount = 0;

  for (const plugin of pluginFiles) {
    try {
      // Read the plugin.json file
      const content = fs.readFileSync(plugin.path, 'utf8');
      const data = JSON.parse(content);

      // Check if the "agents" field exists
      if (!data.hasOwnProperty('agents')) {
        console.log(`✓ ${plugin.name}: No "agents" field - skipped`);
        skippedCount++;
        continue;
      }

      // Remove the "agents" field
      const agentsValue = data.agents;
      delete data.agents;

      // Write back the modified JSON (with 2-space indentation to match original)
      const newContent = JSON.stringify(data, null, 2) + '\n';
      fs.writeFileSync(plugin.path, newContent, 'utf8');

      console.log(`✓ ${plugin.name}: Removed "agents": "${agentsValue}"`);
      fixedCount++;

    } catch (error) {
      console.error(`✗ ${plugin.name}: Error - ${error.message}`);
      errorCount++;
    }
  }

  console.log('\n' + '='.repeat(50));
  console.log('Summary:');
  console.log(`  Fixed: ${fixedCount}`);
  console.log(`  Skipped: ${skippedCount}`);
  console.log(`  Errors: ${errorCount}`);
  console.log('='.repeat(50));
}

fixPluginManifests().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
